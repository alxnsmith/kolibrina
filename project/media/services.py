import os
import re
from django.conf import settings
from . import models


def get_user_avatar_path(instance, filename):
    if ['png', 'jpg', 'jpeg', 'bmp', 'webp', ].__contains__(filename.split('.')[-1]):
        user_path = os.path.join('users', f'user_{instance.user}')
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, user_path)):
            avatarPath = os.path.join(user_path, f'Avatar.{filename.split(".")[-1]}')
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, avatarPath)):
                os.remove(os.path.join(settings.MEDIA_ROOT, avatarPath))
            return avatarPath


def get_avatar(user):
    _create_user_media_dir(user)
    userPath = os.path.join(settings.MEDIA_ROOT, 'users/', f'user_{user}')
    regexAva = re.compile(r'Avatar.(jpg|png|jpeg|bmp|webp)')
    existAva = list(filter(regexAva.search, os.listdir(userPath)))
    if existAva:
        ava = '/'.join([settings.MEDIA_URL[:-1], '/'.join(userPath.split('/')[-2:]), existAva[0]])
    else:
        ava = False
    return ava


def get_banner():
    if models.Banner.objects.filter(name='MainBanner').exists():
        mainBanner = f"{settings.MEDIA_URL}/{str(models.Banner.objects.filter(name='MainBanner')[0].image)}"
    else:
        mainBanner = False
    return mainBanner


def _create_user_media_dir(user):
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'users/', f'user_{user}')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'users/', f'user_{user}'))
