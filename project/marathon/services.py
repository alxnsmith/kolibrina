import random

import redis
from django.conf import settings
from django.utils import timezone

from marathon.models import MarathonRound


def round3(func):
    def wrapper(*args, **kwargs):
        return round(func(*args, **kwargs), 3)

    return wrapper


class MarathonWeekGP:
    """GP: GameProcess"""

    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=settings.REDIS_DB)

    def __init__(self, instance: MarathonRound):
        self.round = instance
        self.marathon_instance = instance.official_marathon_round_set.first()
        self.marathon_id = self.marathon_instance.id
        self.response_timer = self.marathon_instance.response_timer
        self.select_question_timer = self.marathon_instance.select_question_timer

        # self._init_round()
        self._init_questions()
        self.datetime_start = self.round.date_time_start

    def get_base_static_info(self):
        info = {
            'marathon_id': self.marathon_id,
            'firstname': self.round.author.firstName,
            'lastname': self.round.author.lastName,
            'city': self.round.author.city
        }
        return info

    def check_answer(self, block, pos, answer):
        question = self.questions[int(block)][int(pos)]
        return question.correct_answer == answer

    def get_correct_answer(self, coords):
        answer = self.questions[coords[0]][coords[1]].correct_answer
        return answer

    @property
    def theme_blocks_with_id(self):
        themes = self.round.question_blocks.all()
        themes = [(str(block.theme), block.id) for block in themes]
        return themes

    @property
    def players(self):
        return self.round.players.all()

    @staticmethod
    def get_all_question_coords_by_blocks(blocks: int):
        return set([(block, pos) for pos in range(8) for block in range(blocks)])

    def get_all_question_coords(self):
        return set([(block, pos) for pos in range(8) for block in range(len(self.round.question_blocks.all()))])

    def get_random_question(self, active_questions):
        coords = random.choice(list(active_questions))
        question = self.get_question(*coords)
        return question

    def get_question(self, block, pos):
        question = self.questions[block][pos]
        answers = [question.correct_answer, question.answer2, question.answer3, question.answer4]
        random.shuffle(answers)
        question = {
            'question': question.question,
            'answers': answers,
            'block': block,
            'pos': pos
        }
        return question

    def _init_round(self):
        rounds = self.round.rounds.filter(date_time_start__gte=timezone.now()).order_by('date_time_start')
        self.round = rounds.first()

    def _init_questions(self):
        questions_blocks = self.round.question_blocks.all()
        questions = [[question for question in block.questions.all()] for block in questions_blocks]
        self.questions = questions


def get_active_official_marathon_rounds() -> dict:
    active_marafon_rounds = MarathonRound.objects.filter(
        is_active=True, purpose=MarathonRound.Purposes.OFFICIAL, date_time_start__isnull=False,
        official_marathon_round_set__isnull=False
    ).order_by('date_time_start')
    if active_marafon_rounds.exists():
        return {'status': 'OK', 'rounds_list': active_marafon_rounds}
    else:
        return {'status': 'error', 'error': 'Empty'}


def get_nearest_official_marathon_round():
    result = get_active_official_marathon_rounds()
    if result['status'] == 'error':
        return False
    filtered = result['rounds_list'].filter(date_time_start__gte=timezone.now())
    if not filtered.exists():
        return False

    instance = filtered.first()
    return instance
