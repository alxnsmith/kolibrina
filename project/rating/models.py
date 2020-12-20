from django.db import models
from userK.models import User
from games.models import Tournament
from marathon.models import MarathonRound
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from stats.services import get_sym_plus_if_num_is_positive


class ScoreHistoryElement(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    value = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{get_sym_plus_if_num_is_positive(self.value)}{self.value}'

    class Meta:
        verbose_name = _('Элемент истории счета')
        verbose_name_plural = _('Элементы истории счета')


class TournamentWeekScoreUserLink(models.Model):
    score_instance = models.ForeignKey(ScoreHistoryElement, on_delete=models.CASCADE, verbose_name='Счет')
    tournament_instance = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True, verbose_name='Турнир')

    class Meta:
        verbose_name = _('Связь (турнир недели)-(игрок)-(счет)')
        verbose_name_plural = _('Связи (турнир недели)-(игрок)-(счет)')


class MarathonWeekScoreUserLink(models.Model):
    score_instance = models.ForeignKey(ScoreHistoryElement, on_delete=models.CASCADE, verbose_name='Счет')
    round_instance = models.ForeignKey(MarathonRound, on_delete=models.SET_NULL, null=True, verbose_name='Раунд')

    def __str__(self):
        return f'{self.score_instance.player.username} | {self.score_instance} | {self.round_instance}'

    class Meta:
        verbose_name = _('Связь (раунд марафона недели)-(игрок)-(счетом)')
        verbose_name_plural = _('Связи (раунд марафона недели)-(игрок)-(счетом)')
