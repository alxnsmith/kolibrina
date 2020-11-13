import datetime
import random

from django.utils import timezone

from questions.services import get_list_official_marathons
from games.services import get_user_info


def round3(func):
    def wrapper(*args, **kwargs):
        return round(func(*args, **kwargs), 3)

    return wrapper


class MarafonWeek:
    def __init__(self, instance, user):
        self.instance = instance
        self.user = user
        if type(self.instance) is not dict:
            self.themes = [theme
                           for theme in list(self.instance.question_blocks.all().values_list('theme__theme', 'id'))]
            self.players = self.instance.players.all()

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
            'players': [user.username for user in players],
            'response_timer': self.instance.response_timer,
            'choose_timer': self.instance.choose_timer,
            'price': '0' if user['is_benefit_recipient'] else self.instance.price,
            'date_start': str(self.instance.date_time_start.timestamp()),
            'is_time_to_start': timezone.now() > self.instance.date_time_start,
            'number_of_theme_blocks': list(range(0, len(self.instance.question_blocks.all()))),
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
