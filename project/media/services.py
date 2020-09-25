import os
import re
from django.conf import settings
from . import models


def create_avatar(instance, filename):
    user = User(instance.user)
    path = user.choose_avatar(filename)
    return path


def get_avatar(user):
    user = User(user)
    return user.full_avatar_path


def get_banner():
    if models.Banner.objects.filter(name='MainBanner').exists():
        mainBanner = f"{settings.MEDIA_URL}/{str(models.Banner.objects.filter(name='MainBanner')[0].image)}"
    else:
        mainBanner = False
    return mainBanner


class User:
    def __init__(self, username):
        self.username = str(username)
        self.full_user_media_path = self._get_full_user_media_path()
        self._init_user_media_dir()
        self.avatar = self._avatar()
        self.full_avatar_path = self._get_avatar_path()

    def choose_avatar(self, filename):
        def _image_valid(image_name=filename):
            return image_name.split('.')[-1] in ['png', 'jpg', 'jpeg', 'bmp', 'webp', ]

        if _image_valid():
            user_path = os.path.join(*self.full_user_media_path.split('/')[-2:])
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, user_path)):
                avatarPath = os.path.join(user_path, f'Avatar.{filename.split(".")[-1]}')
                if self.avatar:
                    for avatar in self.avatar:
                        os.remove(os.path.join(self.full_user_media_path, avatar))
                return avatarPath

    def _get_full_user_media_path(self):
        media = settings.MEDIA_ROOT
        full_user_media_path = os.path.join(media, 'users', f'user_{self.username}')
        return full_user_media_path

    def _get_avatar_path(self):
        if self.avatar:
            ava = os.path.join(self.full_user_media_path, self.avatar[0])
            return '/' + '/'.join(ava.split('/')[6:])
        else:
            return False

    def _avatar(self):
        regexAva = re.compile(r'Avatar.(jpg|png|jpeg|bmp|webp)')
        existAva = list(filter(regexAva.search, os.listdir(self.full_user_media_path)))
        return existAva

    def _init_user_media_dir(self):
        if not os.path.exists(self.full_user_media_path):
            os.makedirs(self.full_user_media_path)

