from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    genderChoices = (('Male', 'М'), ('Female', 'Ж'))
    parrent_account_id = models.CharField(_('Родительский аккаунт'), default='')
    username = models.CharField(_('Никнейм'), unique=True)
    email = models.EmailField(_('Email'), unique=True)
    firstName = models.CharField(_('Имя'))
    lastName = models.CharField(_('Фамилия'))
    gender = models.CharField(_('Пол'), choices=genderChoices)
    birthday = models.DateField(_('Дата рождения'))
    country = models.CharField(_('Страна'))
    area = models.CharField(_('Область'))
    city = models.CharField(_('Город'))
    phoneNumber = models.CharField(_('Телефон'), unique=True)
    studyPlace = models.CharField(_('Место учебы'))
    schClass = models.CharField(_('Класс/Курс'))
    workPlace = models.CharField(_('Место Работы'))

    balance = models.CharField(_(), default=0.00)

    lvl = models.CharField(_('Уровень'), default=0)
    rating = models.CharField(_('Рейтинг'), default=0)
    league = models.CharField(_('Лига'), default='')
    scoreHistory = models.CharField(_('История счета'), default=[])

    countMaster = models.CharField(_('Счетчик подсказок мастера'), default=0)
    countDelTwoAnsw = models.CharField(_('Счетчик подсказок "Убрать два ответа"'), default=0)
    countChance = models.CharField(_('Счетчик подсказок "Второй шанс"'), default=0)
    countSkipQuest = models.CharField(_('Счетчик пропуска вопроса'), default=0)

    countRights = models.CharField(_('Счетчик правильных ответов'), default=0)
    countWrongs = models.CharField(_('Счетчик неправильныых ответов'), default=0)
    countTotalGames = models.CharField(_('Счетчик игр'), default=0)

    date_joined = models.DateTimeField(_('Дата регистрации'), default=timezone.now)
    child_account = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
