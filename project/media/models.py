from django.db import models
from os import remove, path
from django.conf import settings


def user_directory_path(instance, filename):
    user_directory_path = 'user_{0}/{1}'.format(instance.user, 'Avatar.' + filename.split('.')[-1])
    if path.exists(settings.MEDIA_ROOT.replace('/', '\\') + user_directory_path.replace('/', '\\')):
        remove(settings.MEDIA_ROOT.replace('/', '\\') + user_directory_path.replace('/', '\\'))
    return user_directory_path


class Image(models.Model):
    user = models.CharField(max_length=128, default='NullUserName')
    image = models.ImageField(upload_to=user_directory_path)
