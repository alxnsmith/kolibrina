from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    genderChoices = (('Male', 'М'), ('Female', 'Ж'))
    parrent_account_id = models.CharField(verbose_name='Родительский аккаунт', default='', max_length=20)
    username = models.CharField(verbose_name='Никнейм', unique=True, max_length=30)
    email = models.EmailField(verbose_name='Email', unique=True)
    firstName = models.CharField(verbose_name='Имя', max_length=128)
    lastName = models.CharField(verbose_name='Фамилия', max_length=128)
    gender = models.CharField(verbose_name='Пол', choices=genderChoices, max_length=10)
    birthday = models.DateField(_('Дата рождения'))
    country = models.CharField(verbose_name='Страна', max_length=128)
    area = models.CharField(verbose_name='Область', max_length=128)
    city = models.CharField(verbose_name='Город', max_length=128)
    phoneNumber = models.CharField(verbose_name='Телефон', unique=True, max_length=20)
    studyPlace = models.CharField(verbose_name='Место учебы', max_length=128)
    schClass = models.CharField(verbose_name='Класс/Курс', max_length=10)
    workPlace = models.CharField(verbose_name='Место Работы', max_length=128)

    balance = models.CharField(verbose_name='Баланс', default=0.00, max_length=128)

    lvl = models.CharField(verbose_name='Уровень', default=0, max_length=128)
    rating = models.CharField(verbose_name='Рейтинг', default=0, max_length=128)
    league = models.CharField(verbose_name='Лига', default='', max_length=128)
    scoreHistory = models.TextField(verbose_name='История счета', default=[])

    countMaster = models.CharField(verbose_name='Счетчик подсказок мастера', default=0, max_length=128)
    countDelTwoAnsw = models.CharField(verbose_name='Счетчик подсказок "Убрать два ответа"', default=0, max_length=128)
    countChance = models.CharField(verbose_name='Счетчик подсказок "Второй шанс"', default=0, max_length=128)
    countSkipQuest = models.CharField(verbose_name='Счетчик пропуска вопроса', default=0, max_length=128)

    countRights = models.CharField(verbose_name='Счетчик правильных ответов', default=0, max_length=128)
    countWrongs = models.CharField(verbose_name='Счетчик неправильныых ответов', default=0, max_length=128)
    countTotalGames = models.CharField(verbose_name='Счетчик игр', default=0, max_length=128)

    date_joined = models.DateTimeField(verbose_name='Дата регистрации', default=timezone.now)
    child_account = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
