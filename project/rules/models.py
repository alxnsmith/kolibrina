from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Rule(models.Model):
    orderRules = models.CharField(max_length=100, verbose_name='Порядок', default='')
    ruleTitle = models.CharField(max_length=100, verbose_name='Название', default='')
    ruleDescription = models.TextField(verbose_name='Полный текст', default='')

    def __str__(self):
        return '{0}. {1}'.format(self.orderRules, self.ruleTitle)

    class Meta:
        verbose_name = _('Правило')
        verbose_name_plural = _('Правила')
