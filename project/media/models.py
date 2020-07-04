from django.db import models
from os import remove, path, listdir
from django.conf import settings
from re import match


def user_directory_path(instance, filename):
    user_directory_path = 'users/' + 'user_{0}/'.format(instance.user)
    if path.exists(settings.MEDIA_ROOT.replace('/', '\\') + user_directory_path.replace('/', '\\')):
        avatarFile = match(r'Avatar\.(jpg|png|jpeg)',
                           ' '.join(listdir(settings.MEDIA_ROOT.replace('/', '\\') + user_directory_path)))
        if avatarFile is not None:
            remove(settings.MEDIA_ROOT.replace('/', '\\') + user_directory_path.replace('/', '\\') + avatarFile.group())
    return user_directory_path + 'Avatar.' + filename.split('.')[-1]


# def user_directory_path(instance, filename):
#     user_directory_path = 'users/' + 'user_{0}/{1}'.format(instance.user, 'Avatar.')
#     if path.exists(settings.MEDIA_ROOT.replace('/', '\\') + user_directory_path.replace('/', '\\')):
#         remove(settings.MEDIA_ROOT.replace('/', '\\') + user_directory_path.replace('/', '\\'))
#     return user_directory_path + filename.split('.')[-1]


class Avatar(models.Model):
    user = models.CharField(max_length=128, default='NullUserName')
    image = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return self.user


class Banner(models.Model):
    name = models.CharField(max_length=128, default='Banner', unique=True)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT + 'banners')

    def __str__(self):
        return self.name
