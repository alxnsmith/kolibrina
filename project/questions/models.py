from django.db import models
from userK.models import CustomUser
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Category(models.Model):
    category = models.CharField(max_length=25, verbose_name='Категория')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class Purpose(models.Model):
    purpose = models.CharField(max_length=150, verbose_name='Назначение')

    def __str__(self):
        return self.purpose

    class Meta:
        verbose_name = _('Назначение')
        verbose_name_plural = _('Назначения')


class Theme(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default='0', db_column='category', verbose_name='Категория')
    theme = models.CharField(max_length=50, verbose_name='Тема')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = _('Тема')
        verbose_name_plural = _('Темы')


class Question(models.Model):
    diffChoices = (('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'))

    purpose = models.ForeignKey(Purpose, on_delete=models.SET(get_user_model()), db_column='purpose', default=1, verbose_name='Назначение')
    premoderate = models.BooleanField(default=True, verbose_name='На модерации')

    author = models.ForeignKey(CustomUser, on_delete=models.SET(get_user_model()), db_column='author', verbose_name='Автор', default='0')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default='0', db_column='category', verbose_name='Категория')
    theme = models.ForeignKey(Theme, on_delete=models.DO_NOTHING, default='0', db_column='theme', verbose_name='Тема')
    difficulty = models.CharField(choices=diffChoices, max_length=2, default='30', verbose_name='Сложность')
    question = models.TextField(max_length=350, verbose_name='Вопрос')
    corectAnsw = models.CharField(max_length=64, verbose_name='Правильный ответ')
    answer2 = models.CharField(max_length=64, verbose_name='Ответ2')
    answer3 = models.CharField(max_length=64, verbose_name='Ответ3')
    answer4 = models.CharField(max_length=64, verbose_name='Ответ4')

    def __str__(self):
        return 'ID: {}, Q: {}..., A: {}, D: {}, C: {}, T: {}'.format(self.id,
                                                                     self.question[:50],
                                                                     self.corectAnsw,
                                                                     self.difficulty,
                                                                     self.category,
                                                                     self.theme)

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')
