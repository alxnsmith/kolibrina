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
    _players = {}

    def add_player(self, player_instance) -> None:
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

    def get_top_fifteen(self) -> list:
        players = []
        for i, dictionary in enumerate(sorted(self._players.items(), key=lambda x: x[1]['score'])[:15]):
            dictionary = dictionary[1]
            dictionary['pos'] = i
            players.append(dictionary)
        return players

    def get_top_one(self) -> dict:
        return sorted(self._players.items(), key=lambda x: x[1]['score'])[0][1]


class MarafonWeek(JsonWebsocketConsumer):
    class Roles:
        WATCHER = 'watcher'
        PLAYER = 'player'

    game_info = {'is_started': False, 'marafon_id': None}

    watchers_online = set()
    players_online = set()

    expected_players_stack = set()
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
        self.marathon = services.MarathonWeek(marathon, self.user)

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
        self.update_online(event='connect')
        self.update_rating(event='connect')
        self.send_base_static_info()
        # self.send_themes()
        # self.send_game_history()

        self.response_timer = Timer(self.marathon.instance.response_timer)

        if not self.is_time_to_start:
            self.send_date_time_start()
        # self.start_timer()

    def receive_json(self, content, **kwargs):
        if content['type'] == 'event':
            event = content['event']
            if event == 'select_answer':
                current_question = self.game_history['current_question']
                answer = content['answer']
                block_id = current_question[0]
                pos = current_question[1]

                question = self.marathon.check_answer(block_id, pos, answer)
                self.expected_players_stack.discard(self.username)

            elif event == 'select_question':
                block_id = content['block_id']
                pos = content['pos']
                question = self.marathon.get_question(block_id, pos)
                self.game_history['current_question'] = (block_id, pos)
                self.game_history['questions_played'].add((block_id, pos))

                async_to_sync(self.channel_layer.group_send)(
                    self.GAME_GROUP_NAME,
                    {'type': 'send_selected_question', 'question': question}
                )
            elif event == 'time_to_start':
                if not self.game_info['is_started'] and self.is_time_to_start:
                    self.game_info['is_started'] = True
                    print('GAME IS STARTED!')

    def disconnect(self, message):
        async_to_sync(self.channel_layer.group_discard)(
            self.role,
            self.channel_name
        )
        self.update_online(event='disconnect')
        self.update_rating(event='disconnect')

        if len(self.players_online) < 2 and self.game_info['is_started']:
            self.end_game()

    def send_base_static_info(self, *_):
        info = self.marathon.get_base_static_info()
        self.send_json(content={
            'type': 'static_base_info',
            'info': info
        })

    def send_selected_question(self, event):
        question = event['question']

        self.send_json(content={
            'type': 'selected_question',
            'question': question
        })

    def send_start_timer(self, *_):
        timer = self.response_timer.get_end_time_timer()
        player = self.rating.get_top_one()['username']
        self.send_json(content={
            'type': 'timer',
            'timer': timer,
            'player': player
        })

    def send_themes(self, *_):
        self.send_json(content={
            'type': 'themes_list',
            'themes': self.marathon.theme_blocks_with_id
        })

    def end_game(self):
        self.rating.clear()
        self.players_online.clear()
        self.watchers_online.clear()

        self.game_info['is_started'] = False
        self.game_info['marafon_id'] = None

        self.game_history['current_question'] = tuple()
        self.game_history['questions_played'] = set()

        async_to_sync(self.channel_layer.group_send)(
            self.GAME_GROUP_NAME, {'type': 'send_end_game'}
        )

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
            self.send_json(content={
                'type': 'selected_question',
                'question': question
            })

    def update_rating(self, event):
        def update():
            if event == 'connect':
                self.rating.add_player(self.user)
            elif event == 'disconnect':
                self.rating.remove_player(self.user)
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

    def update_online_watchers(self, *_):
        self.send_json(content={
            'type': 'online_watchers',
            'online': len(self.watchers_online)
        })

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

    @property
    def is_time_to_start(self):
        return self.marathon.instance.date_time_start < timezone.now()
