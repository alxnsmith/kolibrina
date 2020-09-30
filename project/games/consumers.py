import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from django.forms.models import model_to_dict
import random

from questions.models import Tournament
from .services import Game
import redis
from django.conf import settings


class TournamentWeek(WebsocketConsumer):
    game_session: object
    tournament_shortname: str

    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)

    def connect(self):
        self.tournament_shortname = self.scope['url_route']['kwargs']['tournament_name']
        self.accept()
        self.game_session = Game(self.tournament_shortname, self.scope['user'])
        self.send(json.dumps({'type': 'timer_duration',
                              'timer': self.game_session.timer_duration}))
        self.send(json.dumps({'type': 'tournament_author',
                              'author': str(self.game_session.tournament_author)}))

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if 'event' in data:
            if data['event'] == 'start_game':
                self._send_next_question()
                self.game_session.init_attempt()
            if data['event'] == 'respond':
                correct_answer = self.game_session.current_question.correct_answer
                if data['answer'] == correct_answer:
                    self.send(json.dumps({'type': 'answer_result', 'result': 'OK'}))
                    self.send(json.dumps({'type': 'reset_timer'}))
                    self._send_next_question()
                else:
                    self.send(json.dumps({'type': 'answer_result', 'result': 'WRONG', 'correct_answer': correct_answer}))

    def send_timer_duration(self, event):
        self.send(text_data=json.dumps(event))

    def _send_next_question(self):
        question, question_num = self.game_session.next_question()
        self.send(json.dumps({'type': 'question', 'question': question, 'question_num': question_num}))