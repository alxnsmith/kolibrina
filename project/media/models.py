from django.db import models
from . import services
from django.utils.translation import ugettext_lazy as _


class Banner(models.Model):
    name = models.CharField(max_length=128, default='main_banner', unique=True)
    image = models.ImageField(upload_to='banners')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Баннер')
        verbose_name_plural = _('Баннеры')
