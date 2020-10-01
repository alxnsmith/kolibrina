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
    last_difficulty = 0
    chance = 0
    hints_quantity = 4
    score_saves = 0
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)

    @property
    def correct_answer(self):
        return self.game_session.current_question.correct_answer

    def connect(self):
        self.tournament_shortname = self.scope['url_route']['kwargs']['tournament_name']
        self.accept()
        self.game_session = Game(self.tournament_shortname, self.scope['user'])
        self.send(json.dumps({'type': 'timer_duration',
                              'timer': self.game_session.timer_duration}))
        self.send(json.dumps({'type': 'tournament_author',
                              'author': str(self.game_session.tournament_author)}))
        if self.game_session.attempt == 3:
            self.send(json.dumps({'type': 'many_attempts'}))

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if 'event' in data:
            if data['event'] == 'start_game':
                if self.game_session.attempt < 3:
                    self.game_session.time_delta()
                    self._send_next_question(self.game_session.next_question())
                    self.game_session.init_attempt()
                else:
                    self.send(json.dumps({'type': 'many_attempts'}))

            elif data['event'] == 'master_hint':
                self.send(json.dumps({'type': 'saved_score', 'score': self.game_session.score.save_bonuses()}))
                self.hints_quantity -= 1
                self.game_session.time_delta(event='reset')
                self.game_session.time_delta()
                self.send(json.dumps({'type': 'master_say',
                                      'speech': 'Мастер считает, что правильный ответ'
                                                f': {self.correct_answer}'}))
                self.send(json.dumps({'type': 'reset_timer'}))
                self.send(json.dumps({'type': 'start_timer'}))
            elif data['event'] == 'fifty-fifty_hint':
                self.send(json.dumps({'type': 'saved_score', 'score': self.game_session.score.save_bonuses()}))
                self.hints_quantity -= 1
                self.game_session.time_delta(event='reset')
                self.game_session.time_delta()
                to_del = self.game_session.prepare_question_to_send(fifty_fifty=True)
                self.send(json.dumps({'type': 'fifty-fifty',
                                      'to_del': f'{to_del}'
                                      }))
                self.send(json.dumps({'type': 'reset_timer'}))
                self.send(json.dumps({'type': 'start_timer'}))
            elif data['event'] == 'skip_hint':
                self.send(json.dumps({'type': 'saved_score', 'score': self.game_session.score.save_bonuses()}))
                self.hints_quantity -= 1
                self.game_session.time_delta(event='reset')
                self.game_session.time_delta()
                zamena = self.game_session.zamena()
                self._send_next_question(zamena)
                self.send(json.dumps({'type': 'reset_timer'}))
                self.send(json.dumps({'type': 'start_timer'}))
            elif data['event'] == 'chance_hint':
                self.send(json.dumps({'type': 'saved_score', 'score': self.game_session.score.save_bonuses()}))
                self.hints_quantity -= 1
                self.game_session.time_delta(event='reset')
                self.game_session.time_delta()
                self.chance += 1
                self.send(json.dumps({'type': 'reset_timer'}))
                self.send(json.dumps({'type': 'start_timer'}))
            elif data['event'] == 'save_score':
                saved_score = self.game_session.score.save()
                self.send(json.dumps({'type': 'saved_score', 'score': saved_score}))
                self.score_saves += 1
                if self.score_saves == 3:
                    self.chance = 0
                    self._answer(correct_answer=self.game_session.current_question.correct_answer)

            elif data['event'] == 'next_question':
                self.send(json.dumps({'type': 'log', 'log': [self.game_session.score.bonus]}))

                self.game_session.time_delta()
                self._send_next_question(self.game_session.next_question())
            elif data['event'] == 'respond':
                timer = self.game_session.time_delta()
                if timer < self.game_session.timer_duration:
                    self._answer(answer=data['answer'], correct_answer=self.game_session.current_question.correct_answer)
                    difficulty = self.game_session.current_question.difficulty
                    saved_time = self.game_session.timer_duration - timer
                    question_pos = self.game_session.current_question.pos

                    self.score = self.game_session.score.value

                    score = self.game_session.score.init(self.last_difficulty, difficulty, self.hints_quantity, saved_time, question_pos)
                    self.send(json.dumps({'type': 'current_score', 'score': score}))
                    self.last_difficulty = difficulty
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
        self.score = self.game_session.score.total()
        if answer == correct_answer:
            self.game_session.time_delta(event='reset')
            self.send(json.dumps({'type': 'answer_result', 'result': 'OK'}))
            self.send(json.dumps({'type': 'reset_timer'}))
            if int(self.game_session.current_question_num) == 24:
                self.send(json.dumps({'type': 'win', 'score': self.score}))
        elif self.chance > 0:
            self.game_session.time_delta()
            self.send(json.dumps({'type': 'chance'}))
            self.chance = 0
        else:
            user = self.scope['user']
            question_num = int(self.game_session.current_question_num)
            if question_num < 8:
                attempts = self.game_session.tournament_model.attempt_set.get(user=user)
                attempts.attempt = 3
                attempts.save()

            self.send(json.dumps({'type': 'answer_result', 'result': 'WRONG', 'correct_answer': correct_answer,
                                  'answer': answer, 'score': self.score}))
