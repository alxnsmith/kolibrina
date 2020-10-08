from django.db import models
from stats.models import ScoreHistoryElement
from userK.models import User
from questions.models import Tournament
from django.utils.translation import ugettext_lazy as _


class TournamentScoreUserLink(models.Model):
    user_instance = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Игрок')
    score_instance = models.ForeignKey(ScoreHistoryElement, on_delete=models.CASCADE, verbose_name='Счет')
    tournament_instance = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING, verbose_name='Турнир')

    class Meta:
        verbose_name = _('Связь между турниром, игроком и счетом')
        verbose_name_plural = _('Связи между турниром, игроком и счетом')