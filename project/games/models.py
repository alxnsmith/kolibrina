from django.db import models
from stats.models import ScoreHistoryElement
from userK.models import User
from questions.models import MarafonThemeBlock, Question
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class Tournament(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя турнира', blank=True)

    class Purposes(models.TextChoices):
        NONE = 'NONE', _('Не указано')
        TRAIN_ER_LOTTO = 'TEL', _('Тренировка эрудит-лото')
        TOURNAMENT_WEEK_ER_LOTTO = 'TWEL', _('Турнир недели эрудит-лото')

    purpose = models.CharField(verbose_name='Назначение', max_length=128, choices=Purposes.choices,
                               default=Purposes.NONE)
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


class Marafon(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя марафона', blank=True)

    class Purposes(models.TextChoices):
        NONE = 'NONE', _('Не указано')
        MARAFON_WEEK_ER_LOTTO = 'MWEL', _('Марафон недели эрудит-лото')

    purpose = models.CharField(verbose_name='Назначение', max_length=128, choices=Purposes.choices,
                               default=Purposes.NONE)
    author = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL,
                               verbose_name="Автор марафона")
    official = models.BooleanField(default=False)
    question_blocks = models.ManyToManyField(MarafonThemeBlock, limit_choices_to={'is_active': True})
    response_timer = models.SmallIntegerField(verbose_name='Время на ответ', default=30)
    choose_timer = models.SmallIntegerField(verbose_name='Время на выбор вопроса', default=15)

    date_time_start = models.DateTimeField(verbose_name='Дата и время проведения', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активный марафон', default=False)

    create_date = models.DateField(verbose_name='Дата создания', default=timezone.now)

    price = models.SmallIntegerField(null=True, blank=True, verbose_name='Цена')
    players = models.ManyToManyField(User, related_name='players', blank=True)

    def __str__(self):
        return f'A: {self.is_active};Name: {self.name}; Author: {self.author}; Create date: {self.create_date}'

    class Meta:
        verbose_name = _('Марафоны')
        verbose_name_plural = _('Марафоны')


class TournamentScoreUserLink(models.Model):
    user_instance = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Игрок')
    score_instance = models.ForeignKey(ScoreHistoryElement, on_delete=models.CASCADE, verbose_name='Счет')
    tournament_instance = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True, verbose_name='Турнир')

    class Meta:
        verbose_name = _('Связь между турниром, игроком и счетом')
        verbose_name_plural = _('Связи между турниром, игроком и счетом')
