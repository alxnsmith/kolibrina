import random

from django.forms.models import model_to_dict
from django.utils import timezone

import datetime
from stats.services import get_sum_score_user
from userK import services as user_services
from questions.models import Tournament, Attempt
from questions.services import get_questions_from_tournament


def create_render_data_for_tournament_week_el(request):
    user = request.user
    avatar_image = user_services.media_services.get_avatar(user)
    last_month_date_range = (timezone.now()-datetime.timedelta(days=30), timezone.now())
    month_score = get_sum_score_user(user, last_month_date_range)
    league = request.user.get_league_display()
    level = user_services.get_user_rating_lvl_dif(user.rating)
    quest_nums = [str(i).rjust(2, '0') for i in range(1, 25)]
    return {'status': 'OK',
            'level': level,
            'AvatarImage': avatar_image,
            'month_score': month_score,
            'quest_nums': quest_nums,
            'league': league}
    # else:
    #     return {'status': 'error', 'error': "This tournament doesn't exist"}


def create_render_data_for_train_el(request):
    quest_nums = [str(i).rjust(2, '0') for i in range(1, 13)]
    return {'status': 'OK',
            'quest_nums': quest_nums,
            'title': 'ТРЕНИРОВКА ЭРУДИТ-ЛОТО',
            'hide_start': True
            }


class Game:
    def __init__(self, tournament_shortname, user, lose_question=0):
        self.lose_question = lose_question
        self.tournament_model = _get_tournament_model(tournament_shortname)
        self.player = user
        self.current_question_num = self._get_start_answer_number()
        self.questions_queryset = get_questions_from_tournament(self.tournament_model)

        self._get_attempt()

        self.question_positions = _gen_pos_question(self.attempt, lose_question)
        self.timer_duration = self.tournament_model.timer
        self.current_question = None
        self.tournament_author = self._get_tournament_author()

        self.current_question_num_gen = self._get_next_answer_number()
        self.current_question_num_gen.send(None)

    def get_timer_duration(self):
        return self.tournament_model.timer

    def next_question(self):
        position = next(self.question_positions)
        self.current_question = self._get_question(position)
        question = self._prepare_question_to_send()
        return question, next(self.current_question_num_gen)

    def _get_next_answer_number(self):
        while int(self.current_question_num) < 25:
            yield self.current_question_num
            self.current_question_num = str(int(self.current_question_num) + 1).rjust(2, '0')
            print('self.current_question_num')

    def _get_tournament_author(self):
        user = self.tournament_model.author
        if user.hideMyName:
            return user.username
        else:
            return f'{user.firstName} {user.lastName}, {user.city}'

    def _get_start_answer_number(self):
        num = self.lose_question
        if num > 7:
            return str(num - 5).rjust(2, '0')
        else:
            return '00'

    def init_attempt(self):
        self._get_attempt()
        if self.attempt == 1:
            self._get_attempt(changes=True)
        else:
            self._get_attempt(changes=True)

    def _get_attempt(self, changes=False):
        attempts = self.player.attempt_set.filter(tournament=self.tournament_model)
        if attempts.exists():
            attempt = attempts[0]
            if changes:
                self._increase_quantity_used_attempts(attempt)
            self.attempt = attempt.attempt
        else:
            self.attempt = 1
            if changes:
                self._create_attempts()

    def _create_attempts(self):
        Attempt.objects.create(tournament=self.tournament_model, user=self.player, attempt=1)

    @staticmethod
    def _increase_quantity_used_attempts(attempt):
        if attempt.attempt < 3:
            attempt.attempt += 1
            attempt.save()

    def _get_question(self, pos):
        return self.questions_queryset.get(pos=pos)

    def _prepare_question_to_send(self):
        question = model_to_dict(self.current_question)
        question['answers'] = [question['correct_answer'],
                               question['answer2'],
                               question['answer3'],
                               question['answer4']]
        del question['correct_answer'], question['answer2'], question['answer3'], question['answer4']
        random.shuffle(question['answers'])
        return question


def _get_tournament_model(tournament_shortname):
    date_range = (timezone.now() - timezone.timedelta(days=7), timezone.now())  # last 7 days
    active_tournaments_list = Tournament.objects.filter(
        is_active=True, destination=tournament_shortname,
        date__range=date_range)
    tournament_model = active_tournaments_list.order_by('date')[0]
    return tournament_model


def _gen_pos_question(attempt, lose_question):
    pos_list = list(range(1, 25))
    d1 = ['d1.1', 'd1.2', 'd1.3', 'd1.4', 'd1.5']
    d2 = ['d2.1', 'd2.2', 'd2.3', 'd2.4', 'd2.5']
    if attempt == 2:
        pos_list = d1 + pos_list[lose_question:]
    elif attempt == 3:
        pos_list = d2 + pos_list[lose_question:]
    for i in pos_list:
        yield i