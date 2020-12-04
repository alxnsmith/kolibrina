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
        full_rating = []
        for i, dictionary in enumerate(sorted(self._players.items(), key=lambda x: x[1]['score'], reverse=True)):
            dictionary = dictionary[1]
            dictionary['pos'] = i
            full_rating.append(dictionary)
        return full_rating

    def get_top_fifteen(self) -> list:
        players = self.get_full_rating()[:15]
        return players

    def get_top_one(self) -> dict:
        return self.get_full_rating()[1]

    def rating_iter(self):
        rating = self.get_full_rating()
        for user in rating:
            yield user

    def reset_delta(self):
        for username in self._players:
            self._players.get(username)['score_delta'] = 0

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

    class States:
        READY_TO_START = 0
        PAUSE = 1
        ANSWER = 2
        QUESTION = 3
        RESULTS = 4
        TIMEOUT = 5

    game_info = {
        'round_exists': False,
        'is_started': False,
        'STATE': States.READY_TO_START,
        'marathon_id': int(),
        'current_question': None,
        'end_timer': int(),
        'timer': None
    }

    game_history = {'current_question': tuple(), 'questions_played': set()}

    deactivated_questions = set()

    watchers_online = set()
    players_online = set()

    expected_answer_players_stack = set()
    correctly_answered_players_stack = set()
    wrong_answered_players_stack = set()

    rating = MarafonRating()

    GAME_GROUP_NAME = 'marathon_week'

    def connect(self):

        self.user = self.scope['user']
        if not (round_instance := services.get_is_played_official_marathon_round()):
            round_instance = services.get_nearest_official_marathon_round()

        if round_instance:
            self.round = services.MarathonWeekGP(round_instance)

            marathon_id = self.round.marathon_id
            if current_id := self.game_info['marathon_id']:
                if current_id != marathon_id:
                    self.end_game()  # resets the current game
            self.game_info['marathon_id'] = marathon_id

            self.username = self.user.username

            if self.user in self.round.players:
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

            self.game_info['is_started'] = self.round.instance.is_played
            self.game_info['round_exists'] = True

        self.accept()

        if not self.game_info['is_started']:
            if not round_instance or self.round.datetime_start < timezone.now():
                self.send_json(content={
                    'type': 'no_events'
                })
                return

        self.send_json(content={'type': 'username', 'username': self.username})
        self.send_json(content={'type': 'role', 'role': self.role})
        self.update_online(event='connect')
        self.update_rating(event='connect')
        self.send_base_static_info()
        self.send_themes()
        if self.game_info['timer']:
            self.send_json(content=self.game_info['timer'])

        #################################################################################

        # print(self.game_history)
        print(self.game_info)

        # ttt = [(3, 4), (3, 1), (3, 7), (0, 2), (0, 5), (2, 2), (1, 0), (1, 6), (1, 3), (3, 0), (3, 3), (3, 6),
        #        (0, 1), (0, 7), (2, 4), (1, 2), (0, 4), (2, 1), (2, 7), (1, 5), (3, 2), (
        #            3, 5), (0, 0), (1, 1), (1, 4), (0, 6), (2, 3), (1, 7), (2, 6)]
        # self.test = set()
        # for t in ttt:
        #     self.deactivated_questions.add(t)
        #     self.game_history['questions_played'].add(t)
        # self.game_history['current_question'] = ttt[2]

        # self.next_step()

        # async_to_sync(self.channel_layer.group_send)(
        #     self.GAME_GROUP_NAME,
        #     {'type': 'send_rating'}
        # )

        # self.rating.incr_score(self.username, 100)

        #################################################################################

        self.send_game_history()

        self.response_timer = Timer(self.round.response_timer)
        if self.round.datetime_start > timezone.now():
            self.send_date_time_start()

    def receive_json(self, content, **kwargs):
        if content['type'] == 'event':
            event = content['event']
            if event == 'select_answer' \
                    and self.username in self.expected_answer_players_stack:

                current_question = self.game_history['current_question']
                answer = content['answer']
                block = current_question[0]
                pos = current_question[1]

                answer_is_true = self.round.check_answer(block, pos, answer)
                if answer_is_true:
                    self.correctly_answered_players_stack.add(self.username)
                else:
                    self.wrong_answered_players_stack.add(self.username)

                self.expected_answer_players_stack.discard(self.username)
                if len(self.expected_answer_players_stack) < 1:
                    self.next_step()

            elif event == 'select_question' \
                    and self.username == self._get_top_one_online():

                async_to_sync(self.channel_layer.group_send)(
                    self.GAME_GROUP_NAME,
                    {'type': 'send_reset_timer'}
                )

                for player in self.players_online:
                    self.expected_answer_players_stack.add(player)
                self.correctly_answered_players_stack.clear()
                self.wrong_answered_players_stack.clear()

                coords = (int(content['block']), int(content['pos']))
                self.select_question(coords)

            elif event == 'time_to_start' \
                    and self.game_info['STATE'] is self.States.READY_TO_START \
                    and not self.game_info['is_started'] \
                    and self.round.datetime_start < timezone.now():
                self.next_step()
                print('GAME IS STARTED!')

            elif event == 'select_question_timer_is_end' \
                    and self.game_info['STATE'] == self.States.QUESTION:

                async_to_sync(self.channel_layer.group_send)(
                    self.GAME_GROUP_NAME,
                    {'type': 'send_reset_timer'}
                )

                for player in self.players_online:
                    self.expected_answer_players_stack.add(player)
                self.correctly_answered_players_stack.clear()
                self.wrong_answered_players_stack.clear()

                self.select_random_question()

            elif event == 'select_answer_timer_is_end' \
                    and self.game_info['STATE'] == self.States.ANSWER:

                self.next_step()

    def disconnect(self, message):
        if self.game_info['round_exists']:
            async_to_sync(self.channel_layer.group_discard)(
                self.role,
                self.channel_name
            )
            self.update_online(event='disconnect')
            self.update_rating(event='disconnect')

        if len(self.players_online) < 2 and self.game_info['is_started']:
            self.end_game()

    def next_step(self):
        if self.game_info['STATE'] not in (self.States.READY_TO_START, self.States.ANSWER):
            return

        if self.game_info['STATE'] is self.States.READY_TO_START and self.round.starter_username_or_none:
            starter = self.round.starter_username_or_none
            round = self.round.instance
            round.is_played = self.game_info['is_started'] = True
            round.save()
        else:
            starter = self._get_top_one_online()

        self.game_info['STATE'] = self.States.QUESTION

        if self.game_info.get('current_question', False):
            cost = (self.game_info['current_question']['pos'] + 1) * 100

            correct_answers = self.correctly_answered_players_stack
            delta_score_for_correct = cost / len(correct_answers) if len(correct_answers) != 0 else 0
            wrong_answers = self.wrong_answered_players_stack
            delta_score_for_wrong = cost / len(wrong_answers) if len(wrong_answers) != 0 else 0

            self.rating.reset_delta()
            for username in correct_answers:
                self.rating.incr_score(username, delta_score_for_correct)
            for username in wrong_answers:
                self.rating.decr_score(username, delta_score_for_wrong)
            async_to_sync(self.channel_layer.group_send)(
                self.GAME_GROUP_NAME,
                {'type': 'send_correct_answer'}
            )

        async_to_sync(self.channel_layer.group_send)(
            self.GAME_GROUP_NAME,
            {'type': 'send_rating'}
        )
        async_to_sync(self.channel_layer.group_send)(
            self.GAME_GROUP_NAME,
            {'type': 'send_reset_timer'}
        )

        if len(self.active_questions) < 1:
            print('Not enough active questions.')
            self.end_game()
            return

        async_to_sync(self.channel_layer.group_send)(
            self.GAME_GROUP_NAME,
            {'type': 'send_select_question',
             'username': starter}
        )

    def send_base_static_info(self, *_):
        info = self.round.get_base_static_info()
        self.send_json(content={
            'type': 'static_base_info',
            'info': info
        })

    def send_select_question(self, event):
        username = event['username']
        select_question_end_time = timezone.now() + timezone.timedelta(seconds=self.round.select_question_timer)
        self.game_info['end_timer'] = select_question_end_time
        self.game_info['timer'] = {
            'type': 'select_question',
            'username': username,
            'timer': str(select_question_end_time)
        }
        self.send_json(content=self.game_info['timer'])

    def select_random_question(self):

        question = self.round.get_random_question(self.active_questions)
        coords = (question['block'], question['pos'])
        self.select_question(coords)

    def send_correct_answer(self, *_):
        correct_answer = self.round.get_correct_answer(self.game_history['current_question'])
        self.send_json(content={
            'type': 'correct_answer',
            'correct_answer': correct_answer
        })

    def select_question(self, coords: tuple) -> None:
        self.game_info['STATE'] = self.States.ANSWER
        question = self.round.get_question(*coords)
        self.game_info['current_question'] = question
        self.deactivated_questions.add(coords)
        self.game_history['current_question'] = coords
        self.game_history['questions_played'].add(coords)

        async_to_sync(self.channel_layer.group_send)(
            self.GAME_GROUP_NAME,
            {'type': 'send_answer_timer'})

        async_to_sync(self.channel_layer.group_send)(
            self.GAME_GROUP_NAME,
            {'type': 'send_selected_question', 'question': question})

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
            'themes': self.round.theme_blocks_with_id
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
        self.deactivated_questions.clear()

        self.game_info['round_exists'] = False
        self.game_info['is_started'] = False
        self.game_info['STATE'] = self.States.READY_TO_START
        self.game_info['marathon_id'] = int()
        self.game_info['end_timer'] = int()
        self.game_info['timer'] = None
        self.game_info['current_question'] = None

        self.game_history['current_question'] = tuple()
        self.game_history['questions_played'] = set()

        if round := self.round.instance:
            round.is_played = False
            round.save()

    def send_end_game(self, *_):
        self.send_json(content={
            'type': 'end_game'
        })

    def send_game_history(self, *_):
        game_history = list(self.game_history['questions_played'])
        current_question = self.game_history['current_question']
        if game_history:
            game_history.remove(current_question)
            question = self.round.get_question(*current_question)
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
        unix_time = str(self.round.instance.date_time_start)
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

    def send_answer_timer(self, *_):
        response_end_time = timezone.now() + timezone.timedelta(seconds=self.round.response_timer)
        self.game_info['end_timer'] = response_end_time
        self.game_info['timer'] = {
            'type': 'answer_timer',
            'unix_time_end': str(response_end_time),
        }
        self.send_json(content=self.game_info['timer'])

    def _get_top_one_online(self):
        rating = self.rating.rating_iter()
        for user in rating:
            username = user['username']
            if username in self.players_online:
                return username
        else:
            self.end_game()

    @property
    def active_questions(self):
        return self.round.get_all_question_coords() - self.deactivated_questions
