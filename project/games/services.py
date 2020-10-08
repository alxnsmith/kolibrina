import datetime
import random
import time

from django.forms.models import model_to_dict
from django.utils import timezone
from django.conf import settings

from questions.models import Attempt
from questions.services import get_questions_from_tournament
from stats.services import get_sum_score_user
from userK import services as user_services
from stats.services import UserScore
from .models import TournamentScoreUserLink


def round3(func):
    def wrapper(*args, **kwargs):
        return round(func(*args, **kwargs), 3)
    return wrapper


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


def create_render_data_for_train_el():
    quest_nums = [str(i).rjust(2, '0') for i in range(1, 13)]
    return {'status': 'OK',
            'quest_nums': quest_nums,
            'title': 'ТРЕНИРОВКА ЭРУДИТ-ЛОТО',
            'hide_start': True
            }


class TournamentWeekInstance:
    def __init__(self, tournament_instance, user, win_bonus=29, lose_question=0):
        self.score = ScoreTournamentWeek(question_score_equals=settings.QUESTION_SCORE_EQUALS,
                                         time_score_equals=settings.TIME_SCORE_EQUALS,
                                         win_bonus=win_bonus)
        self.lose_question = lose_question
        self.tournament_instance = tournament_instance
        self.player_instance = user
        self.player_score_instance = UserScore(self.player_instance)
        self.current_question_num = self._get_start_answer_number()
        self.questions_queryset = get_questions_from_tournament(self.tournament_instance)
        
        self._get_attempt()

        self.pos_list = self.init_pos_list(self.attempt + 1, self.lose_question)
        self.next_question_pos = self._gen_pos_question(self.pos_list)
        self.timer_duration = self.tournament_instance.timer
        self.tournament_author = self._get_tournament_author()

        self.current_question_num_gen = self._get_next_question_number()
        self.current_question_num_gen.send(None)

        self.current_question = None
        self.timer = None

        self.is_started = False

    @property
    def correct_answer(self):
        return self.current_question.correct_answer

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

    def end_game(self, score):
        if self.is_started:
            player_score_instance = self.player_score_instance
            user = self.player_instance
            tournament_instance = self.tournament_instance
            score_link_instance = tournament_instance.tournamentscoreuserlink_set
            score_link_query_set = score_link_instance.filter(user_instance=user)
            if 8 < int(self.current_question_num):
                if 8 < int(self.current_question_num):
                    self.attempt_instance.attempt2 = True
                if 12 < int(self.current_question_num):
                    self.attempt_instance.attempt3 = True
                self.attempt_instance.save()

            if score_link_query_set.exists():
                score_instance = score_link_query_set[0].score_instance
                score_instance.score = score
                score_instance.save()
            else:
                score_instance = player_score_instance.add(score)
                score_link_instance.create(user_instance=user,
                                           score_instance=score_instance,
                                           tournament_instance=tournament_instance)

    def _get_next_question_number(self):
        quantity_questions = 25
        while int(self.current_question_num) < quantity_questions:
            yield self.current_question_num
            self.current_question_num = str(int(self.current_question_num) + 1).rjust(2, '0')

    def _get_tournament_author(self):
        user = self.tournament_instance.author
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
        self._get_attempt(changes=True)

    def _get_attempt(self, changes=False):
        attempts = self.player_instance.attempt_set.filter(tournament=self.tournament_instance)
        if attempts.exists():
            attempt = self.attempt_instance = attempts[0]
            self.attempt2 = attempts[0].attempt2
            self.attempt3 = attempts[0].attempt3
            if changes:
                self._increase_quantity_used_attempts(attempt)
            self.attempt = attempt.attempt
        else:
            self.attempt = 0
            if changes:
                self.attempt_instance = self._create_attempts()

    def _create_attempts(self):
        return Attempt.objects.create(tournament=self.tournament_instance, user=self.player_instance, attempt=1)

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


class ScoreTournamentWeek:
    def __init__(self, question_score_equals, time_score_equals, win_bonus=29):
        self.question_score_equals = question_score_equals
        self.time_score_equals = time_score_equals
        self.quantity_saved_hints = 4
        self.question_pos = 0
        self.prev_question_difficulty = 0
        self.saved_time = 0
        self.combo = 0
        self.question_difficulty = 0
        self.win_bonus = win_bonus

        self.score_saves_left = 3

        self.combo_bonus = 0
        self.current_total_combo_bonus = 0
        self.time_bonus = 0
        self.current_total_time_bonus = 0
        self.question_score = 0
        self.current_total_question_score = 0
        self.saved_bonus_score = 0
        self.saved_question_score = 0

    @round3
    def init_and_get_current_score(self, question_pos, saved_time, question_difficulty):
        if question_pos != 'zamena':
            self.question_pos = question_pos
            self.prev_question_difficulty = self.question_difficulty
            self.saved_time = int(saved_time)
            self.question_difficulty = int(question_difficulty)

            self.current_total_combo_bonus += self.combo_bonus_on_question
            self.current_total_time_bonus += self.time_bonus_on_question
            self.current_total_question_score += self.question_score_on_question
            self.combo_bonus += self.combo_bonus_on_question
            self.time_bonus += self.time_bonus_on_question
            self.question_score += self.question_score_on_question
        return self.current_score

    def save_and_get_saved_score(self):
        self.saved_bonus_score += self.combo_bonus + self.time_bonus
        self.saved_question_score += self.question_score
        self.combo_bonus = 0
        self.time_bonus = 0
        self.question_score = 0
        self.score_saves_left -= 1
        return {'saved_score': round(self.saved_score + self.hint_bonus, 3), 'saves_left': self.score_saves_left}

    def hint_used_and_get_saved_score(self):
        self.saved_bonus_score += self.combo_bonus + self.time_bonus
        self.time_bonus = 0
        self.combo_bonus = 0
        self.combo_reset()
        self.hints_decr()
        
        return round(self.current_score, 3), round(self.saved_score, 3)

    def hints_decr(self):
        self.quantity_saved_hints -= 1

    def combo_incr(self):
        self.combo += 1

    def combo_reset(self):
        self.combo = 0

    @property
    @round3
    def saved_score(self):
        return self.saved_question_score + self.saved_bonus_score

    @property
    @round3
    def lose(self):
        return self.saved_score + self.time_bonus + self.hint_bonus + self.combo_bonus

    @property
    @round3
    def win(self):
        return self.current_score + self.win_bonus

    @property
    @round3
    def current_score(self):
        return self.current_total_combo_bonus + self.current_total_time_bonus \
               + self.current_total_question_score + self.hint_bonus

    @property
    @round3
    def hint_bonus(self):
        return round(self.quantity_saved_hints * 0.2 * self.prev_question_difficulty, 3)

    @property
    @round3
    def question_score_on_question(self):
        return self.question_score_equals[self.question_pos]

    @property
    @round3
    def time_bonus_on_question(self):
        return self.saved_time * self.time_score_equals[str(self.question_difficulty)]

    @property
    @round3
    def combo_bonus_on_question(self):
        return (self.combo - 1) * (self.question_difficulty + int(str(self.question_pos).split('.')[-1])) / (
                70 - self.question_difficulty)
