from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from questions.models import MarathonThemeBlock
from games.models import BaseGame, BaseRound
from userK.models import User


class BaseMarathon(BaseGame):
    response_timer = models.SmallIntegerField(verbose_name='Время на ответ', default=30)
    select_question_timer = models.SmallIntegerField(verbose_name='Время на выбор вопроса', default=20)

    class Meta:
        abstract = True


class MarathonRound(BaseRound):
    class Purposes(models.IntegerChoices):
        OFFICIAL = 0, 'Оффициальный'
        COMMUNITY = 1, 'Пользовательский'

    purpose = models.SmallIntegerField('Назначение', choices=Purposes.choices, default=Purposes.OFFICIAL)

    question_blocks = models.ManyToManyField(
        MarathonThemeBlock, verbose_name='Блоки вопросов', limit_choices_to={'is_active': True})

    is_played = models.BooleanField('Сейчас играют', default=False)

    players = models.ManyToManyField(
        User, verbose_name='Зарегистрированные игроки', blank=True, related_name='MarathonRound_players_set')
    starter_player = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='starter_player_in_marathon_week', null=True, blank=True,
        verbose_name='Стартер'
    )

    def __str__(self):
        return f'ID: {self.id}, Create date: {self.create_date}'

    class Meta:
        verbose_name = _('Раунд марафона')
        verbose_name_plural = _('Раунды марафона')


class MarathonWeekOfficial(BaseMarathon):
    rounds = models.ManyToManyField(MarathonRound, verbose_name='Раунды', related_name='official_marathon_round_set')
    stage = models.SmallIntegerField('Этап', null=False, default=0)

    is_rating = models.BooleanField(verbose_name='Рейтинговый', default=False)

    class Meta:
        verbose_name = _('Официальный марафон')
        verbose_name_plural = _('Официальные марафоны')


class MarathonWeekCommunity(BaseMarathon):
    round = models.ForeignKey(MarathonRound, on_delete=models.SET_NULL, null=True, verbose_name='Игровой раунд')

    class Meta:
        verbose_name = _('Пользовательский марафон')
        verbose_name_plural = _('Полльзовательские марафоны')

