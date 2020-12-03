from django.db import models
from userK.models import User
from .services import get_sym_plus_if_num_is_positive, get_sum_from_history, init_league
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class ScoreHistoryElement(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    value = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} | {}{}'.format(self.player.username,
                                  get_sym_plus_if_num_is_positive(self.value),
                                  self.value)

    class Meta:
        verbose_name = _('Элемент истории счета')
        verbose_name_plural = _('Элементы истории счета')


class RatingHistoryElement(models.Model):
    player = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=False)
    value = models.IntegerField('Рейтинг')
    date = models.DateTimeField('Дата', default=timezone.now)

    def __str__(self):
        return '{} | {}{}'.format(self.player.username,
                                  get_sym_plus_if_num_is_positive(self.value),
                                  self.value)

    def _init_user(self):
        self.player.rating = get_sum_from_history(self.player.ratinghistoryelement_set)
        init_league(self.player)

    def save(self, *args, **kwargs):
        super(RatingHistoryElement, self).save(*args, **kwargs)
        self._init_user()
        self.player.save()

    def delete(self, using=None, keep_parents=False):
        super(RatingHistoryElement, self).delete()
        self._init_user()
        self.player.save()

    class Meta:
        verbose_name = _('Элемент истории рейтинга')
        verbose_name_plural = _('Элементы истории рейтинга')
