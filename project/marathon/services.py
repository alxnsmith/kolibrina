import random

import redis
from django.conf import settings

from marathon.models import MarathonWeekOfficial


def round3(func):
    def wrapper(*args, **kwargs):
        return round(func(*args, **kwargs), 3)

    return wrapper


class MarathonWeek:
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=settings.REDIS_DB)

    def __init__(self, instance, round_number):
        self.instance = instance
        self.datetime_start = self.instance.date_time_start
        self.response_timer = instance.response_timer
        self.select_question_timer = instance.select_question_timer
        self.id = instance.id

        self._rounds = [rounds for rounds in instance.rounds.all()]
        self.set_round(round_number)

    def get_base_static_info(self):
        info = {
            'marathon_id': self.id,
            'firstname': self.instance.author.firstName,
            'lastname': self.instance.author.lastName,
            'city': self.instance.author.city
        }
        return info

    def check_answer(self, block, pos, answer):
        question = self.questions[int(block)][int(pos)]
        return question.correct_answer == answer

    @property
    def theme_blocks_with_id(self):
        themes = self.round.question_blocks.all()
        themes = [(str(block.theme), block.id) for block in themes]
        return themes

    @property
    def players(self):
        return self.instance.players.all()

    @staticmethod
    def get_all_question_coords():
        return set([(block, pos) for pos in range(8) for block in range(4)])

    def get_all_question_coords2(self):
        return set([(block, pos) for pos in range(8) for block in range(len(self._rounds)+1)])

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

    def set_round(self, round_number):
        self.round = self._rounds[round_number]
        self._init_questions()

    def _init_questions(self):
        questions_blocks = self.round.question_blocks.all()
        questions = [[question for question in block.questions.all()] for block in questions_blocks]
        self.questions = questions


def get_list_official_marathons() -> dict:
    active_marafon_list = MarathonWeekOfficial.objects.filter(
        is_active=True, date_time_start__isnull=False, code_name__isnull=False
    ).order_by('-date_time_start')

    if active_marafon_list.exists():
        return {'status': 'OK', 'marathons_list': active_marafon_list}
    else:
        return {'status': 'error', 'error': 'Empty'}


def get_official_marathon():
    result = get_list_official_marathons()
    if result['status'] == 'error':
        return

    instance = result['marathons_list'][0]
    marathon = MarathonWeek(instance, 0)
    return marathon
