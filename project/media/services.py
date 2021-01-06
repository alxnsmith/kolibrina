import os
import re
from django.conf import settings
from . import models
from account.models import User as UserModel


def get_banner():
    main_banner = models.Banner.objects.filter(name='main_banner')
    banner = main_banner.first().image.url if main_banner.exists() else False

    return banner


class User:
    def __init__(self, username):
        self.username = str(username)
        self.user = UserModel.objects.get(username=str(username))
        self.full_user_media_path = self._get_full_user_media_path()
        self._init_user_media_dir()
        self.avatar = self.user.avatar.url if self.user.avatar else False

    def _get_full_user_media_path(self):
        media = settings.MEDIA_ROOT
        full_user_media_path = os.path.join(media, 'users', f'user_{self.username}')
        return full_user_media_path

    def _init_user_media_dir(self):
        if not os.path.exists(self.full_user_media_path):
            os.makedirs(self.full_user_media_path)
