from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from questions.models import Question, Purpose
from account.models import User


class Tournament(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя турнира', blank=True)

    purpose = models.ForeignKey(Purpose, verbose_name='Назначение', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL,
                               verbose_name="Автор турнира")
    timer = models.IntegerField(verbose_name='Время таймера', default=30)
    date = models.DateTimeField(verbose_name='Дата и время проведения', blank=True, null=True)
    create_date = models.DateField(verbose_name='Дата создания', default=timezone.now)
    is_active = models.BooleanField(verbose_name="Активный турнир", default=False)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return f'Name: {self.name}; Author: {self.author}; Create date: {self.create_date}'

    class Meta:
        verbose_name = _('Турнир')
        verbose_name_plural = _('Турниры')


class Attempt(models.Model):
    class Attempts(models.IntegerChoices):
        ONE = 1, _('Одна')
        TWO = 2, _('Две')
        THREE = 3, _('Три')

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name='Турнир')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Игрок')
    attempt = models.IntegerField(verbose_name='Попыток совершено', choices=Attempts.choices, default=Attempts.ONE)
    lose_num_question = models.IntegerField(verbose_name='Номер, последнего вопроса', default=0)
    attempt2 = models.BooleanField(verbose_name='Разрешить вторую попытку', default=False)
    attempt3 = models.BooleanField(verbose_name='Разрешить третью попытку', default=False)

    def __str__(self):
        return f'T: {self.tournament}; P: {self.user}, A: {self.attempt}'

    class Meta:
        verbose_name = _('Попытка')
        verbose_name_plural = _('Попытки')


class BaseGame(models.Model):
    name = models.CharField('Название', max_length=128, blank=True, null=True)
    code_name = models.CharField('Кодовое имя', max_length=128, blank=True, null=True)
    price = models.SmallIntegerField('Цена', null=False, default=0)

    is_active = models.BooleanField('Активный', default=False)
    # is active for a round will be used when the admin will set rounds for a game event in custom admin

    create_date = models.DateField('Дата создания', default=timezone.now)
    author = models.ForeignKey(User, null=True, verbose_name='Автор', on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def __str__(self):
        return f'ID: {self.id}, CODE: {self.code_name}, IS_ACTIVE: {self.is_active}'


class BaseRound(models.Model):
    is_active = models.BooleanField('Активный', default=False)
    price = models.SmallIntegerField('Цена', null=False, default=0)
    date_time_start = models.DateTimeField('Дата и время проведения', blank=True, null=True)
    create_date = models.DateField('Дата создания', default=timezone.now)
    author = models.ForeignKey(User, null=True, verbose_name='Автор', on_delete=models.SET_NULL)

    class Meta:
        abstract = True
