from django.db import models
from django.utils.translation import ugettext_lazy as _


class Team(models.Model):
    team_name = models.CharField(max_length=30, unique=True)
    score = models.IntegerField(default=0)
    last_game_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.team_name

    class Meta:
        verbose_name = _('Команда')
        verbose_name_plural = _('Команды')