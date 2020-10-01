import datetime
import random
import time

from django.forms.models import model_to_dict
from django.utils import timezone
from django.conf import settings

from questions.models import Tournament, Attempt
from questions.services import get_questions_from_tournament
from stats.services import get_sum_score_user
from userK import services as user_services


def create_render_data_for_tournament_week_el(request):
    user = request.user
    avatar_image = user_services.media_services.get_avatar(user)
    last_month_date_range = (timezone.now() - datetime.timedelta(days=30), timezone.now())
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


class Score:
    def __init__(self, win_bonus, hints_quantity=4):
        self.last_difficulty = 0
        self.hints_quantity = hints_quantity
        self.combo = 0
        self.num_question_in_current_difficult = 0

        self.win_bonus = win_bonus
        self.question_score_equals = settings.QUESTION_SCORE_EQUALS

        self.per_questions = 0
        self.saved_time = 0
        self.bonus = 0
        self.value = 0

    def total(self):
        total_value = round(self.per_questions + self.saved_time + self.bonus, 3)
        return total_value

    def save_bonuses(self):
        self.value += round(self.bonus + self.saved_time, 3)
        self.saved_time = 0
        self.combo = 0
        self.bonus = 0
        return round(self.value + self.saved_time, 3)

    def exexute(self):
        return round(self.value + self.saved_hints, 3)

    def save(self):
        self.value += self.total()
        self.per_questions = 0
        self.saved_time = 0
        self.bonus = 0
        return round(self.value, 3)

    def increase_saved_time(self, saved_time):
        if int(self.last_difficulty) == 10:
            self.saved_time = round(self.saved_time + saved_time * 0.007, 3)
        elif int(self.last_difficulty) == 20:
            self.saved_time = round(self.saved_time + saved_time * 0.08, 3)
        elif int(self.last_difficulty) == 30:
            self.saved_time = round(self.saved_time + saved_time * 0.14, 3)
        elif int(self.last_difficulty) == 40:
            self.saved_time = round(self.saved_time + saved_time * 0.2, 3)
        elif int(self.last_difficulty) == 50:
            self.saved_time = round(self.saved_time + saved_time * 0.23, 3)

    def increase_bonus(self, question_pos, difficulty):
        self.bonus = round(self.bonus + (self.combo-1)*(int(difficulty) + self._get_num_question_in_current_difficult(question_pos))/(70-int(difficulty)), 3)

    def increase_per_questions(self, question_pos):
        self.per_questions = round(self.per_questions + self.question_score_equals[question_pos], 3)

    @property
    def saved_hints(self):
        return round((int(self.hints_quantity) * int(self.last_difficulty)) / 5, 3)

    def win(self):
        return round(self.total() + self.win_bonus, 3)

    def init(self, last_difficulty, difficulty, hints_quantity, saved_time, question_pos):
        self.increase_bonus(question_pos, difficulty)
        self.last_difficulty = last_difficulty
        self.hints_quantity = hints_quantity
        self.increase_saved_time(saved_time)
        self.increase_per_questions(question_pos)
        self.combo += 1
        return round(self.total() + self.saved_hints, 3)

    @staticmethod
    def _get_num_question_in_current_difficult(question_pos):
        try:
            return int(question_pos)
        except ValueError:
            if question_pos.startswith('d'):
                return int(question_pos[-1])
            else:
                return 1

    def __str__(self):
        return str(self.total())


class Game:
    def __init__(self, tournament_shortname, user, win_bonus=29, lose_question=0):
        self.score = Score(win_bonus=win_bonus)
        self.lose_question = lose_question
        self.tournament_model = self._get_tournament_model(tournament_shortname)
        self.player = user
        self.current_question_num = self._get_start_answer_number()
        self.questions_queryset = get_questions_from_tournament(self.tournament_model)

        self._get_attempt()

        self.pos_list = self.init_pos_list(self.attempt + 1, self.lose_question)
        self.next_question_pos = self._gen_pos_question(self.pos_list)
        self.timer_duration = self.tournament_model.timer
        self.tournament_author = self._get_tournament_author()

        self.current_question_num_gen = self._get_next_question_number()
        self.current_question_num_gen.send(None)

        self.current_question = None
        self.timer = None

    def zamena(self):
        position = 'zamena'
        self.current_question = self._get_question(position)
        question = self.prepare_question_to_send()
        return question

    def time_delta(self, event=None):
        if event == 'reset':
            self.timer = None
        elif event is None:
            if self.timer is None:
                self.timer = int(time.time())
            else:
                self.timer = int(time.time()) - self.timer
                return self.timer

    def next_question(self):
        position = next(self.next_question_pos)
        self.current_question = self._get_question(position)
        question = self.prepare_question_to_send()
        current_question_num = next(self.current_question_num_gen)
        return question, current_question_num

    def _get_next_question_number(self):
        if self.lose_question > 7:
            quantity_questions = 25 - self.lose_question + 5
        else:
            quantity_questions = 25
        while int(self.current_question_num) < quantity_questions:
            yield self.current_question_num
            self.current_question_num = str(int(self.current_question_num) + 1).rjust(2, '0')

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
            self.attempt = 0
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

    def prepare_question_to_send(self, fifty_fifty=False):
        question = model_to_dict(self.current_question)
        question['answers'] = [question['correct_answer'],
                               question['answer2'],
                               question['answer3'],
                               question['answer4']]
        del question['correct_answer'], question['answer2'], question['answer3'], question['answer4']
        if fifty_fifty:
            del question['answers'][0]
            random.shuffle(question['answers'])
            del question['answers'][-1]
            return question['answers']
        random.shuffle(question['answers'])

        return question

    @staticmethod
    def _get_tournament_model(tournament_shortname):
        date_range = (timezone.now() - timezone.timedelta(days=7), timezone.now())  # last 7 days
        active_tournaments_list = Tournament.objects.filter(
            is_active=True, destination=tournament_shortname,
            date__range=date_range)
        tournament_model = active_tournaments_list.order_by('date')[0]
        return tournament_model


    @staticmethod
    def init_pos_list(attempt, lose_question):
        pos_list = list(range(1, 25))
        d1 = ['d1.1', 'd1.2', 'd1.3', 'd1.4', 'd1.5']
        d2 = ['d2.1', 'd2.2', 'd2.3', 'd2.4', 'd2.5']
        if attempt == 2:
            pos_list = d1 + pos_list[lose_question:]
        elif attempt == 3:
            pos_list = d2 + pos_list[lose_question:]
        return pos_list


    @staticmethod
    def _gen_pos_question(pos_list):
        for i in pos_list:
            yield i
