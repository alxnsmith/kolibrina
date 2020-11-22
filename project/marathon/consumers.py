import time

import redis
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings
from django.utils import timezone

from . import services


class Timer:
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=settings.REDIS_DB)

    def __init__(self, timer):
        self.timer = timer

    def get_end_time_timer(self):
        return timezone.now().timestamp() + self.timer


class MarafonRating:
    _players = dict()

    def add_player_or_pass(self, player_instance) -> None:
        if player_instance.username in self._players:
            return

        player = {
            'username': player_instance.username,
            'hide_name': player_instance.hide_my_name,
            'score': 0,
            'score_delta': 0
        }
        if not player['hide_name']:
            player.update({
                'first_name': player_instance.firstName,
                'last_name': player_instance.lastName,
                'city': player_instance.city,
            })
        self._players[player['username']] = player

    def remove_player(self, player_instance) -> None:
        if self._players.get(player_instance.username):
            del self._players[player_instance.username]

    def clear(self):
        self._players.clear()

    def get_full_rating(self) -> list:
        players = []
        for i, dictionary in enumerate(sorted(self._players.items(), key=lambda x: x[1]['score'], reverse=True)):
            dictionary = dictionary[1]
            dictionary['pos'] = i
            players.append(dictionary)
        return players

    def get_top_fifteen(self) -> list:
        players = self.get_full_rating()[:15]
        return players

    def get_top_one(self) -> dict:
        return sorted(self._players.items(), key=lambda x: x[1]['score'])[0][1]

    def rating_iter(self):
        rating = sorted(self._players.items(), key=lambda x: x[1]['score'])
        for user in rating:
            yield user

    def incr_score(self, username, delta):
        player = self._players.get(username)
        player['score'] += delta
        player['score_delta'] = delta

    def decr_score(self, username, delta):
        player = self._players.get(username)
        player['score'] -= delta
        player['score_delta'] = -delta


class MarafonWeek(JsonWebsocketConsumer):
    class Roles:
        WATCHER = 'watcher'
        PLAYER = 'player'

    game_info = {
        'is_started': False,
        'marafon_id': None,
        'response_end_time': None,
        'select_question_end_time': None,
        'current_question': None,
    }

    active_questions = services.MarathonWeek.get_all_question_coords()

    deactivated_questions = set()

    watchers_online = set()
    players_online = set()

    expected_answer_players_stack = set()
    correctly_answered_players_stack = set()
    wrong_answered_players_stack = set()

    rating = MarafonRating()

    game_history = {'current_question': tuple(), 'questions_played': set()}

    GAME_GROUP_NAME = 'marafon_week'

    def connect(self):

        self.user = self.scope['user']

        result = services.get_list_official_marathons()
        if result['status'] == 'error':
            return

        marathon = result['marathons_list'][0]
        self.marathon = services.MarathonWeek(marathon, 0)

        marafon_id = self.marathon.id
        if current_id := self.game_info['marafon_id']:
            if current_id != marafon_id:
                self.end_game()
        self.game_info['marafon_id'] = marafon_id

        self.username = self.user.username

        if self.user in self.marathon.players:
            self.role = self.Roles.PLAYER
        else:
            self.role = self.Roles.WATCHER

        async_to_sync(self.channel_layer.group_add)(
            self.role,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_add)(
            self.GAME_GROUP_NAME,
            self.channel_name
        )

        self.accept()
        self.send_json(content={'type': 'username', 'username': self.username})
        self.send_json(content={'type': 'role', 'role': self.role})
        self.update_online(event='connect')
        self.update_rating(event='connect')
        self.send_base_static_info()
        self.send_themes()

        #################################################################################

        print(self.game_history)
        self.next_step()
        # async_to_sync(self.channel_layer.group_send)(
        #     self.GAME_GROUP_NAME,
        #     {'type': 'send_rating'}
        # )

        # self.rating.incr_score(self.username, 100)

        # self.active_questions = self.marathon.get_all_question_coords2()

        #################################################################################

        self.send_game_history()

        self.response_timer = Timer(self.marathon.instance.response_timer)
        if self.marathon.datetime_start > timezone.now():
            self.send_date_time_start()

    def receive_json(self, content, **kwargs):
        if content['type'] == 'event':
            event = content['event']
            if event == 'select_answer':
                self.send_reset_timer()

                current_question = self.game_history['current_question']
                answer = content['answer']
                block = current_question[0]
                pos = current_question[1]

                answer_is_true = self.marathon.check_answer(block, pos, answer)
                if answer_is_true:
                    self.correctly_answered_players_stack.add(self.username)
                else:
                    self.wrong_answered_players_stack.add(self.username)

                self.expected_answer_players_stack.discard(self.username)
                if len(self.expected_answer_players_stack) < 1:
                    cost = (self.game_info['current_question']['pos']+1)*100

                    correct_answers = self.correctly_answered_players_stack
                    delta_score_for_correct = cost / len(correct_answers) if len(correct_answers) != 0 else 0
                    wrong_answers = self.wrong_answered_players_stack
                    delta_score_for_wrong = cost / len(wrong_answers) if len(wrong_answers) != 0 else 0

                    for username in correct_answers:
                        self.rating.incr_score(username, delta_score_for_correct)
                    for username in wrong_answers:
                        self.rating.decr_score(username, delta_score_for_wrong)

                    async_to_sync(self.channel_layer.group_send)(
                        self.GAME_GROUP_NAME,
                        {'type': 'send_rating'}
                    )

                    self.next_step()

            elif event == 'select_question' and self.username == self._get_top_one_online():
                async_to_sync(self.channel_layer.group_send)(
                    self.GAME_GROUP_NAME,
                    {'type': 'send_reset_timer'}
                )

                block = int(content['block'])
                pos = int(content['pos'])

                for player in self.players_online:
                    self.expected_answer_players_stack.add(player)
                self.correctly_answered_players_stack.clear()
                self.wrong_answered_players_stack.clear()

                question = self.select_question(block, pos)

                async_to_sync(self.channel_layer.group_send)(
                    self.GAME_GROUP_NAME,
                    {'type': 'send_selected_question', 'question': question}
                )
            elif event == 'time_to_start':
                if not self.game_info['is_started'] and self.marathon.datetime_start < timezone.now():
                    self.game_info['is_started'] = True
                    print('GAME IS STARTED!')
                    self.next_step()

    def disconnect(self, message):
        async_to_sync(self.channel_layer.group_discard)(
            self.role,
            self.channel_name
        )
        self.update_online(event='disconnect')
        self.update_rating(event='disconnect')

        if len(self.players_online) < 2 and self.game_info['is_started']:
            self.end_game()

    def next_step(self):
        async_to_sync(self.channel_layer.group_send)(
            self.GAME_GROUP_NAME,
            {'type': 'send_reset_timer'}
        )
        async_to_sync(self.channel_layer.group_send)(
            self.GAME_GROUP_NAME,
            {'type': 'send_select_question',
             'username': self._get_top_one_online()}
        )

    def send_base_static_info(self, *_):
        info = self.marathon.get_base_static_info()
        self.send_json(content={
            'type': 'static_base_info',
            'info': info
        })

    def send_select_question(self, event):
        username = event['username']
        select_question_end_time = timezone.now() + timezone.timedelta(seconds=self.marathon.select_question_timer)
        self.game_info['select_question_end_time'] = select_question_end_time
        self.send_json(content={
            'type': 'select_question',
            'username': username,
            'timer': str(select_question_end_time)
        })

    def select_random_question(self):
        if len(self.active_questions) < 1:
            print('Not enough active questions.')
            return

        question = self.marathon.get_random_question(self.active_questions)
        coord = (question['block'], question['pos'])
        self.active_questions.discard(coord)
        question = self.select_question(*coord)
        async_to_sync(self.channel_layer.group_send)(
            self.GAME_GROUP_NAME,
            {'type': 'send_selected_question', 'question': question}
        )

    def select_question(self, block, pos):
        question = self.marathon.get_question(block, pos)

        self.game_info['current_question'] = question
        self.active_questions.discard((block, pos))
        self.game_history['current_question'] = (block, pos)
        self.game_history['questions_played'].add((block, pos))

        async_to_sync(self.channel_layer.group_send)(
            self.GAME_GROUP_NAME,
            {'type': 'send_respond_timer'})
        return question

    def send_selected_question(self, event):
        question = event['question']

        self.send_json(content={
            'type': 'selected_question',
            'question': question,
            'expected_players': list(self.expected_answer_players_stack)
        })

    def send_themes(self, *_):
        self.send_json(content={
            'type': 'themes_list',
            'themes': self.marathon.theme_blocks_with_id
        })

    def end_game(self):
        self.reset()
        async_to_sync(self.channel_layer.group_send)(
            self.GAME_GROUP_NAME, {'type': 'send_end_game'}
        )

    def reset(self):
        self.rating.clear()
        self.players_online.clear()
        self.watchers_online.clear()

        self.game_info['is_started'] = False
        self.game_info['marafon_id'] = None

        self.game_history['current_question'] = tuple()
        self.game_history['questions_played'] = set()

    def send_end_game(self, *_):
        self.send_json(content={
            'type': 'end_game'
        })

    def send_game_history(self, *_):
        game_history = list(self.game_history['questions_played'])
        current_question = self.game_history['current_question']
        if game_history:
            game_history.remove(current_question)
            question = self.marathon.get_question(*current_question)
            self.send_json(content={
                'type': 'game_history',
                'game_history': game_history
            })
            self.send_selected_question({'question': question})

    def update_rating(self, event):
        def update():
            if event == 'connect':
                self.rating.add_player_or_pass(self.user)
            # elif event == 'disconnect':
            #     self.rating.remove_player(self.user)
            async_to_sync(self.channel_layer.group_send)(
                self.GAME_GROUP_NAME,
                {'type': 'send_rating'})

        if self.role == self.Roles.PLAYER:
            update()
        else:
            self.send_rating()

    def send_rating(self, *_):
        self.send_json(content={
            'type': 'top_fifteen',
            'rows': self.rating.get_top_fifteen()
        })

    def update_online(self, event):
        def update(group, group_name):
            if event == 'connect':
                group.add(self.user.username)
            elif event == 'disconnect':
                group.discard(self.user.username)
            async_to_sync(self.channel_layer.group_send)(
                self.GAME_GROUP_NAME,
                {'type': f'update_online_{group_name}s'})

        if self.role == self.Roles.WATCHER:
            update(self.watchers_online, self.Roles.WATCHER)
            self.update_online_players()
        elif self.role == self.Roles.PLAYER:
            update(self.players_online, self.Roles.PLAYER)
            self.update_online_watchers()

    def update_online_players(self, *_):
        self.send_json(content={
            'type': 'online_players',
            'online': len(self.players_online)
        })

    def send_date_time_start(self, *_):
        unix_time = str(self.marathon.instance.date_time_start)
        self.send_json(content={
            'type': 'date_time_start',
            'date_time_start': unix_time
        })

    def update_online_watchers(self, *_):
        self.send_json(content={
            'type': 'online_watchers',
            'online': len(self.watchers_online)
        })

    def send_reset_timer(self, *_):
        self.send_json({'type': 'reset_timer'})

    def send_stop_timer(self, *_):
        self.send_json({'type': 'stop_timer'})

    def send_respond_timer(self, *_):
        response_end_time = timezone.now() + timezone.timedelta(seconds=self.marathon.response_timer)
        self.game_info['response_end_time'] = response_end_time
        self.send_json(content={
            'type': 'respond_timer',
            'unix_time_end': str(response_end_time),
        })

    def _get_top_one_online(self):
        rating = self.rating.rating_iter()
        for user in rating:
            username = user[0]
            if username in self.players_online:
                return username
        else:
            self.end_game()
