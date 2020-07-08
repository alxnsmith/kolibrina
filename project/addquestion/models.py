from django.db import models
from userK.models import CustomUser
from django.contrib.auth import get_user_model


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Category(models.Model):
    category = models.CharField(max_length=25)

    def __str__(self):
        return self.category


class Theme(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default='0', db_column='category')
    theme = models.CharField(max_length=50)

    def __str__(self):
        return self.theme


class Questions(models.Model):
    diffChoices = (('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'))

    premoderate = models.BooleanField(default=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET(get_user_model()), db_column='username')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default='0', db_column='category')
    theme = models.ForeignKey(Theme, on_delete=models.DO_NOTHING, default='0', db_column='theme')
    difficulty = models.CharField(choices=diffChoices, max_length=2, default='30')
    question = models.TextField(max_length=350)
    corectAnsw = models.CharField(max_length=64)
    answer2 = models.CharField(max_length=64)
    answer3 = models.CharField(max_length=64)
    answer4 = models.CharField(max_length=64)

    def __str__(self):
        return 'Вопрос: {0}..., Ответ: {1}, Сложность: {2}'.format(self.question[:50], self.corectAnsw, self.difficulty)
