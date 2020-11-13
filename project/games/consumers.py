import json

import redis
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from django.conf import settings
from django.utils import timezone

from questions.services import get_tournament_instance
from . import services


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
        self.tournament_instance = get_tournament_instance(self.tournament_shortname)
        self.accept()
        self.game_session = services.TournamentWeekInstance(self.tournament_instance, self.scope['user'],
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

