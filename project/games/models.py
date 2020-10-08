from django.db import models
from stats.models import ScoreHistory
from userK.models import User
from questions.models import Tournament


class TournamentScoreUserLink(models.Model):
    user_instance = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Игрок')
    score_instance = models.ForeignKey(ScoreHistory, on_delete=models.CASCADE, verbose_name='Счет')
    tournament_instance = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING, verbose_name='Турнир')
