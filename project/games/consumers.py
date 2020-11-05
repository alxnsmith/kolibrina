import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from django.utils import timezone
from django.forms.models import model_to_dict
import random
import math

from questions.models import Tournament
from .services import TournamentWeekInstance, get_marafon_instance, user_services
import redis
from django.conf import settings


class TournamentWeek(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_session = None
        self.tournament_shortname = None
        self.current_question_and_question_num = None
        self.tournament_instance = None
        self.chance = 0
        self.hints_quantity = 4
        self.score_saves = 0
        self.current_question_num = 0
        self._lose_num_question = 0

    @property
    def lose_num_question(self):
        attempts = self.scope['user'].attempt_set.filter(tournament=self.tournament_instance)
        if attempts.exists():
            attempt = attempts[0]
            self._lose_num_question = attempt.lose_num_question
        return self._lose_num_question

    @property
    def correct_answer(self):
        return self.game_session.correct_answer

    def connect(self):
        self.tournament_shortname = self.scope['url_route']['kwargs']['tournament_name']
        self.tournament_instance = _get_tournament_instance(self.tournament_shortname)
        self.accept()
        self.game_session = TournamentWeekInstance(self.tournament_instance, self.scope['user'],
                                                   lose_question=self.lose_num_question)
        self.send(json.dumps({'type': 'timer_duration',
                              'timer': self.game_session.timer_duration}))
        self.send(json.dumps({'type': 'tournament_author',
                              'author': str(self.game_session.tournament_author)}))
        attempt = self.game_session.attempt
        if attempt > 0:
            attempt2 = self.game_session.attempt2
            if attempt > 0 and not attempt2:
                self.send(json.dumps({'type': 'many_attempts'}))
            attempt3 = self.game_session.attempt3
            if attempt > 1 and not attempt3:
                self.send(json.dumps({'type': 'many_attempts'}))
            if attempt == 3:
                self.send(json.dumps({'type': 'many_attempts'}))

    def disconnect(self, code):
        if code == 1001:
            if self.game_session.is_started:
                data = {'event': 'respond', 'answer': None}
                self.check_respond(data)

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if 'event' in data:
            if data['event'] == 'start_game':
                if self.game_session.attempt < 3:
                    self.game_session.time_delta()
                    self.current_question_and_question_num = self.game_session.next_question()
                    self.current_question_num = int(self.current_question_and_question_num[1])
                    self._send_next_question(self.current_question_and_question_num)
                    self.game_session.init_attempt()
                    self.game_session.is_started = True
                else:
                    self.send(json.dumps({'type': 'many_attempts'}))

            elif data['event'].endswith('_hint'):
                current_score, saved_score = self.game_session.score.hint_used_and_get_saved_score()
                self.send(json.dumps({'type': 'saved_score', 'score': saved_score}))
                self.send(json.dumps({'type': 'current_score', 'score': current_score}))
                self.hints_quantity -= 1
                self.game_session.time_delta(event='reset')
                self.game_session.time_delta()
                self.send(json.dumps({'type': 'restart_timer'}))
                if data['event'] == 'master_hint':
                    self.send(json.dumps({'type': 'master_say',
                                          'speech': f'Мастер считает, что правильный ответ: {self.correct_answer}'}))
                elif data['event'] == 'fifty-fifty_hint':
                    to_del = self.game_session.prepare_question_to_send(fifty_fifty=True)
                    self.send(json.dumps({'type': 'fifty-fifty', 'to_del': f'{to_del}'}))
                elif data['event'] == 'skip_hint':
                    zamena = self.game_session.zamena()
                    self._send_next_question(zamena)
                elif data['event'] == 'chance_hint':
                    self.chance += 1

            elif data['event'] == 'save_score':
                saved_score = self.game_session.score.save_and_get_saved_score()
                self.send(json.dumps({'type': 'saved_score', 'score': saved_score['saved_score']}))
                if saved_score['saves_left'] == 0:
                    self.chance = 0
                    self._answer(correct_answer=self.game_session.current_question.correct_answer)

            elif data['event'] == 'next_question':
                self.game_session.time_delta()
                self.current_question_and_question_num = self.game_session.next_question()
                self.current_question_num = int(self.current_question_and_question_num[1])
                self._send_next_question(self.current_question_and_question_num)

            elif data['event'] == 'respond':
                self.check_respond(data)

    def check_respond(self, data):
        timer = self.game_session.time_delta()
        if timer < self.game_session.timer_duration:
            result = self._answer(answer=data['answer'],
                                  correct_answer=self.game_session.current_question.correct_answer)
            difficulty = self.game_session.current_question.difficulty
            saved_time = self.game_session.timer_duration - timer
            question_pos = self.game_session.current_question.pos

            current_score = self.game_session.score.init_and_get_current_score(
                question_pos=question_pos,
                saved_time=saved_time,
                question_difficulty=difficulty)

            if result['status'] == 'CORRECT':
                self.game_session.score.combo_incr()
                self.send(json.dumps({'type': 'current_score', 'score': current_score}))
            elif result['status'] == 'WRONG':
                score = self.game_session.score.lose
                self.send(json.dumps({
                    'type': 'answer_result', 'result': 'WRONG', 'correct_answer': self.correct_answer,
                    'answer': data['answer'], 'score': score}))
                self.game_session.end_game(score)
            elif result['status'] == 'WIN':
                score = self.game_session.score.win
                self.game_session.player_score_instance.add(score)
                self.send(json.dumps({'type': 'win', 'score': score}))
                self.game_session.end_game(score)
        else:
            self._answer(correct_answer=self.game_session.current_question.correct_answer)

    def send_timer_duration(self, event):
        self.send(text_data=json.dumps(event))

    def _send_next_question(self, question):
        if isinstance(question, tuple):
            question, question_num = question
        else:
            question_num = question['pos']
        if question_num != 'zamena':
            self.send(json.dumps({'type': 'question', 'question': question, 'question_num': question_num}))
        else:
            self.send(json.dumps({'type': 'zamena', 'question': question}))

    def _answer(self, correct_answer='', answer=None):
        def wrong():
            user = self.scope['user']
            attempts = self.game_session.tournament_instance.attempt_set.get(user=user)
            attempts.lose_num_question = self.current_question_num
            attempts.save()
            return {'status': 'WRONG'}

        def chance():
            self.game_session.time_delta()
            self.send(json.dumps({'type': 'chance'}))
            self.chance = 0
            return {'status': 'CHANCE'}

        if answer is None:
            return wrong()
        if answer == correct_answer:
            self.game_session.time_delta(event='reset')
            self.send(json.dumps({'type': 'answer_result', 'result': 'OK'}))
            self.send(json.dumps({'type': 'reset_timer'}))
            if int(self.current_question_num) == 24:
                user = self.scope['user']
                attempts = self.game_session.tournament_instance.attempt_set.get(user=user)
                attempts.lose_num_question = self.current_question_num
                attempts.attempt = 3
                attempts.save()
                return {'status': 'WIN'}
            return {'status': 'CORRECT'}
        elif self.chance > 0:
            return chance()
        else:
            return wrong()


def _get_tournament_instance(tournament_shortname):
    date_range = (timezone.now() - timezone.timedelta(days=7), timezone.now())  # last 7 days
    active_tournaments_list = Tournament.objects.filter(
        is_active=True, purpose=tournament_shortname,
        date__range=date_range)
    tournament_model = active_tournaments_list.order_by('date')[0]
    return tournament_model


class Timer:
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=settings.REDIS_DB)

    def __init__(self, timer):
        self.timer = timer

    def get_end_time_timer(self):
        return timezone.now().timestamp() + self.timer


class MarafonRating:
    players = {}

    def add_player(self, player_instance) -> None:
        player = {
            'username': player_instance.username,
            'hide_name': player_instance.hideMyName,
            'score': 0,
            'score_delta': 0
        }
        if not player['hide_name']:
            player.update({
                'first_name': player_instance.firstName,
                'last_name': player_instance.lastName,
                'city': player_instance.city,
            })
        self.players[player['username']] = player

    def remove_player(self, player_instance) -> None:
        if self.players.get(player_instance.username):
            del self.players[player_instance.username]

    def get_top_fifteen(self) -> list:
        players = []
        for i, dictionary in enumerate(sorted(self.players.items(), key=lambda x: x[1]['score'])[:15]):
            dictionary = dictionary[1]
            dictionary['pos'] = i
            players.append(dictionary)
        return players


class MarafonWeek(JsonWebsocketConsumer):
    class Roles:
        WATCHER = 'watcher'
        PLAYER = 'player'

    game_info = {'is_started': False}

    watchers_online = set()
    players_online = set()
    rating = MarafonRating()
    marafon = get_marafon_instance()

    themes = [theme
              for theme in list(marafon.question_blocks.all().values_list('theme__theme', 'theme'))]

    GAME_GROUP_NAME = 'marafon_week'

    def connect(self):
        print(self.game_info)
        self.user = self.scope['user']

        self.username = self.user.username

        if self.user in self.marafon.players.all():
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

        for i in range(0, 4):
            theme = list(self.marafon.question_blocks.all().values_list('theme__theme', 'theme'))[i]
            for raw_question in list(self.marafon.question_blocks.all())[i].questions.all():
                question = {'question': raw_question.question,
                            'correct_answer': raw_question.correct_answer,
                            'answer2': raw_question.answer2,
                            'answer3': raw_question.answer3,
                            'answer4': raw_question.answer4,
                            'pos': raw_question.pos,
                            'author': raw_question.author,

                            }

        self.send_themes()

        self.response_timer = Timer(self.marafon.response_timer)
        # self.start_timer()

    def receive_json(self, content, **kwargs):
        print(content)
        if content['type'] == 'event':
            if content['event'] == 'time_to_start':
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

    def send_start_timer(self, *_):
        self.send_json({'type': 'timer', 'timer': self.response_timer.get_end_time_timer()})

    def send_themes(self, *_):
        self.send_json({'type': 'themes_list', 'themes': self.themes})

    def end_game(self):
        self.game_info['is_started'] = False
        async_to_sync(self.channel_layer.group_send)(
            self.GAME_GROUP_NAME,
            {'type': 'send_end_game'}
        )

    def send_end_game(self, *_):
        self.send_json({
            'type': 'end_game'
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
        self.send_json({'type': 'top_fifteen', 'rows': self.rating.get_top_fifteen()})

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
        self.send_json(content={'type': 'online_watchers', 'online': len(self.watchers_online)})

    def update_online_players(self, *_):
        self.send_json(content={'type': 'online_players', 'online': len(self.players_online)})

    @property
    def is_time_to_start(self):
        return self.marafon.date_time_start < timezone.now()
