from django.db import models
from django.utils.translation import ugettext_lazy as _

from account.models import User


class Team(models.Model):
    name = models.CharField(max_length=30, unique=True)
    score = models.IntegerField(default=0)
    last_game_date = models.DateField(blank=True, null=True)
    players = models.ManyToManyField(User)
    invites = models.ManyToManyField(User, related_name='invites_set')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Команда')
        verbose_name_plural = _('Команды')
