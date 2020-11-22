from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from questions.models import MarathonThemeBlock
from games.models import BaseGame
from userK.models import User


class BaseMarathon(BaseGame):
    response_timer = models.SmallIntegerField(verbose_name='Время на ответ', default=30)
    select_question_timer = models.SmallIntegerField(verbose_name='Время на выбор вопроса', default=20)

    class Meta:
        abstract = True


class MarathonRound(models.Model):
    question_blocks = models.ManyToManyField(MarathonThemeBlock, limit_choices_to={'is_active': True})

    create_date = models.DateField(verbose_name='Дата создания', default=timezone.now)

    def __str__(self):
        return f'ID: {self.id}, Create date: {self.create_date}'

    class Meta:
        verbose_name = _('Раунд марафона')
        verbose_name_plural = _('Раунды марафона')


class MarathonWeekOfficial(BaseMarathon):
    price = models.SmallIntegerField(null=True, blank=True, verbose_name='Цена')
    rounds = models.ManyToManyField(MarathonRound, verbose_name='Раунды')

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='OELMW_author')
    is_rating = models.BooleanField(verbose_name='Рейтинговый', default=False)

    class Meta:
        verbose_name = _('Официальный марафон')
        verbose_name_plural = _('Официальные марафоны')


class MarathonWeekCommunity(BaseMarathon):
    user_starter = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='user_starter', verbose_name='Стартер')
    round = models.ForeignKey(MarathonRound, on_delete=models.SET_NULL, null=True, verbose_name='Игровой раунд')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='CELMW_author')

    class Meta:
        verbose_name = _('Пользовательский марафон')
        verbose_name_plural = _('Полльзовательские марафоны')
