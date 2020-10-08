from django.db import models
from userK.models import User
from .services import get_sym_plus_if_num_is_positive
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class ScoreHistoryElement(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    score = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} | {}{}'.format(self.player.username,
                                  get_sym_plus_if_num_is_positive(self.score),
                                  self.score)

    def save(self, *args, **kwargs):
        super(ScoreHistoryElement, self).save(*args, **kwargs)
        self.player.save()

    def delete(self, using=None, keep_parents=False):
        super(ScoreHistoryElement, self).delete()
        self.player.save()

    class Meta:
        verbose_name = _('Элемент истории счета')
        verbose_name_plural = _('Элементы истории счета')