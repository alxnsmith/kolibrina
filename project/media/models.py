from django.db import models
from . import services


class Avatar(models.Model):
    user = models.CharField(max_length=128, default='NullUserName')
    image = models.ImageField(upload_to=services.create_avatar)

    def __str__(self):
        return self.user


class Banner(models.Model):
    name = models.CharField(max_length=128, default='MainBanner', unique=True)
    image = models.ImageField(upload_to='banners')

    def __str__(self):
        return self.name
