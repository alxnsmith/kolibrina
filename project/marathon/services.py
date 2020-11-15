import datetime
import random

from django.utils import timezone

from games.services import get_user_info
from marathon.models import MarathonWeekOfficial


def round3(func):
    def wrapper(*args, **kwargs):
        return round(func(*args, **kwargs), 3)

    return wrapper


class MarathonWeek:
    def __init__(self, instance, user):
        self.instance = instance
        self.user = user

    @property
    def info(self) -> dict:
        if type(self.instance) is dict and self.instance['status'] == 'error':
            return self.instance
        players = self.instance.players.all()
        user = get_user_info(self.user)
        user['is_player'] = self.user in players
        return {
            'status': 'OK',
            'id': self.instance.id,
            'name': self.instance.name,
            'author': self.instance.author.username,
            'author_firstname': self.instance.author.firstName,
            'author_lastname': self.instance.author.lastName,
            'author_city': self.instance.author.city,
            'response_timer': self.instance.response_timer,
            'choose_timer': self.instance.choose_timer,
            'price': '0' if user['is_benefit_recipient'] else self.instance.price,
            'date_start': str(self.instance.date_time_start.timestamp()),
            'user': user
        }

    def get_question(self, block_id, pos):
        questions = self.instance.question_blocks.get(id=block_id).questions.all()
        question = questions.get(pos=pos)
        answers = [question.correct_answer, question.answer2, question.answer3, question.answer4]
        random.shuffle(answers)
        question = {
            'question': question.question,
            'answers': answers,
            'block_id': block_id,
            'pos': pos
        }
        return question


def get_list_official_marathons() -> dict:
    active_marafon_list = MarathonWeekOfficial.objects.filter(
        is_active=True, date_time_start__isnull=False, code_name__isnull=False
    ).order_by('-date_time_start')

    if active_marafon_list.exists():
        return {'status': 'OK', 'marathons_list': active_marafon_list}
    else:
        return {'status': 'error', 'error': 'Empty'}
