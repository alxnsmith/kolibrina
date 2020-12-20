import random

import redis
from django.conf import settings
from django.utils import timezone

from marathon.models import MarathonRound, MarathonWeekOfficial


def round3(func):
    def wrapper(*args, **kwargs):
        return round(func(*args, **kwargs), 3)

    return wrapper


class MarathonWeekGP:
    """GP: GameProcess"""

    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=settings.REDIS_DB)

    def __init__(self, instance: MarathonRound, date_time_start):
        self.instance = instance
        self.marathon_instance = instance.marathonweekofficial_set.first()
        self.is_continuous = self.marathon_instance.is_continuous

        if self.is_continuous:
            self.rounds = self.marathon_instance.rounds.order_by('date_time_start')
            self.stage = self.marathon_instance.stage

        self.marathon_id = self.marathon_instance.id
        self.response_timer = self.marathon_instance.response_timer
        self.select_question_timer = self.marathon_instance.select_question_timer
        self.starter_username_or_none = instance.starter_player.username if instance.starter_player else None

        # self._init_round()
        self._init_questions()
        self.date_time_start = date_time_start

    def get_base_static_info(self):
        info = {
            'marathon_id': self.marathon_id,
            'firstname': self.instance.author.firstName,
            'lastname': self.instance.author.lastName,
            'city': self.instance.author.city
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
        themes = self.instance.question_blocks.all()
        themes = [(str(block.theme), block.id) for block in themes]
        return themes

    @property
    def players(self):
        if self.is_continuous:
            return self.marathon_instance.players.all()
        return self.instance.players.all()

    @staticmethod
    def get_all_question_coords_by_blocks(blocks: int):
        return set([(block, pos) for pos in range(8) for block in range(blocks)])

    def get_all_question_coords(self):
        return set([(block, pos) for pos in range(8) for block in range(len(self.instance.question_blocks.all()))])

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
        rounds = self.instance.rounds.filter(date_time_start__gte=timezone.now()).order_by('date_time_start')
        self.instance = rounds.first()

    def _init_questions(self):
        questions_blocks = self.instance.question_blocks.all()
        questions = [[question for question in block.questions.all()] for block in questions_blocks]
        self.questions = questions


def get_active_official_marathon_rounds():
    active_marafon_rounds = MarathonRound.objects.filter(
        purpose=MarathonRound.Purposes.OFFICIAL, date_time_start__isnull=False,
        marathonweekofficial_set__isnull=False, marathonweekofficial_set__is_active=True,
        date_time_start__gte=timezone.now()
    ).order_by('date_time_start')
    return active_marafon_rounds


def get_is_played_official_marathon_round():
    active_official_rounds = MarathonRound.objects.filter(
        purpose=MarathonRound.Purposes.OFFICIAL,
        marathonweekofficial_set__isnull=False,
        marathonweekofficial_set__is_active=True)
    is_played_rounds = active_official_rounds.filter(is_played=True)
    if is_played_rounds.exists():
        round_instance = is_played_rounds.first()
        date_time_start = round_instance.date_time_start

        if (marathon_instance := round_instance.marathonweekofficial_set).exists():
            date_time_start = marathon_instance.first().date_time_start

        return {'instance': round_instance, 'date_time_start': date_time_start}
    else:
        return False


def get_nearest_official_continuous_marathons():
    base_query = {'is_active': True, 'date_time_start__isnull': False, 'is_continuous': True}
    nearest_continuous_marathon = None
    expected = MarathonWeekOfficial.objects.filter(**base_query, date_time_start__gte=timezone.now())

    ends_time = timezone.now() - timezone.timedelta(minutes=10)
    started = MarathonWeekOfficial.objects.filter(
        **base_query, ends_time__isnull=False, ends_time__gte=ends_time)
    if expected or started:
        nearest_continuous_marathon = expected.union(started).order_by('date_time_start')
    return nearest_continuous_marathon


def get_nearest_official_marathon_round():
    round = continuous_marathon = False

    active_rounds = get_active_official_marathon_rounds()
    filtered_active_rounds = active_rounds.filter(date_time_start__gte=timezone.now())
    if filtered_active_rounds.exists():
        round = filtered_active_rounds.first()

    filtered_continuous_marathon = get_nearest_official_continuous_marathons()
    if filtered_continuous_marathon.exists():
        continuous_marathon = filtered_continuous_marathon.first()

    if round and continuous_marathon:
        instance = round if round.date_time_start < continuous_marathon.date_time_start else continuous_marathon
    else:
        instance = round or continuous_marathon

    if isinstance(instance, MarathonWeekOfficial):
        stage = instance.stage
        round_instance =\
            instance.rounds.order_by('date_time_start')[stage] if stage < instance.rounds.count() else None
        if instance.stage == 0:
            date_time_start = timezone.localtime(instance.date_time_start)
        else:
            date_time_start = timezone.localtime(instance.ends_time + timezone.timedelta(minutes=10))
    else:
        round_instance = instance
        date_time_start = timezone.localtime(instance.date_time_start)

    if round_instance:

        return {'instance': round_instance, 'date_time_start': date_time_start}
    else:
        return False
