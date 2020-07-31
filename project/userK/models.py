from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    genderChoices = (('Male', 'М'), ('Female', 'Ж'))
    countryChoices = (('RU', 'Россия'), ('UK', 'Украина'), ('BY', 'Беларусь'), ('KZ', 'Казахстан'))
    parrent_account_id = models.CharField(verbose_name='Родительский аккаунт', default='', max_length=20, blank=True)
    child_account = models.BooleanField(verbose_name='Детский аккаунт', default=False)
    username = models.CharField(verbose_name='Никнейм', unique=True, max_length=30)
    is_active = models.BooleanField(verbose_name='Активация аккаунта', default=False)
    email = models.EmailField(verbose_name='Email', unique=True)
    firstName = models.CharField(verbose_name='Имя', max_length=128)
    lastName = models.CharField(verbose_name='Фамилия', max_length=128)
    hideMyName = models.BooleanField(verbose_name='Скрыть имя и фамилию', default=False)
    balance = models.CharField(verbose_name='Баланс', default=0.00, max_length=128)

    gender = models.CharField(verbose_name='Пол', choices=genderChoices, max_length=10)
    birthday = models.DateField(verbose_name='Дата рождения', null=True)
    country = models.CharField(verbose_name='Страна', choices=countryChoices, max_length=128)
    area = models.CharField(verbose_name='Область', max_length=128)
    city = models.CharField(verbose_name='Город', max_length=128)
    phoneNumber = models.CharField(verbose_name='Телефон', unique=True, max_length=20, null=True)
    swPlace = models.CharField(
        verbose_name='Место работы / учёбы: ВУЗ / колледж / школа - класс', max_length=128, blank=True
    )

    opLVL = models.CharField(verbose_name='Опыт(Очки уровня)', default=0, max_length=128)
    league = models.CharField(verbose_name='Лига', choices=(
        ('l1', 'Школьная лига'), ('l2', 'Лига колледжей'), ('l3', 'Студенческая лига'),
        ('l4', 'Высшая лига'), ('l5', 'Премьер-лига'), ('l6', 'Супер-лига')),
        blank=True, max_length=128)
    scoreHistory = models.TextField(verbose_name='История счета', default=[])

    countMaster = models.CharField(verbose_name='Счетчик подсказок мастера', default=0, max_length=128)
    countDelTwoAnsw = models.CharField(verbose_name='Счетчик подсказок "Убрать два ответа"', default=0, max_length=128)
    countChance = models.CharField(verbose_name='Счетчик подсказок "Второй шанс"', default=0, max_length=128)
    countSkipQuest = models.CharField(verbose_name='Счетчик пропуска вопроса', default=0, max_length=128)

    countRights = models.CharField(verbose_name='Счетчик правильных ответов', default=0, max_length=128)
    countWrongs = models.CharField(verbose_name='Счетчик неправильныых ответов', default=0, max_length=128)
    countTotalGames = models.CharField(verbose_name='Счетчик игр', default=0, max_length=128)

    date_joined = models.DateTimeField(verbose_name='Дата регистрации', default=timezone.now)
    last_game = models.DateTimeField(verbose_name='Дата последней игры', default=timezone.now)
    is_staff = models.BooleanField(verbose_name='Администратор', default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
