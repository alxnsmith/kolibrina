from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from media.models import Avatar
from stats.services import init_league
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    # personal data
    username = models.CharField('Никнейм', unique=True, max_length=30)
    firstName = models.CharField('Имя', max_length=128)
    lastName = models.CharField('Фамилия', max_length=128)
    gender = models.CharField('Пол', choices=settings.GENDER_CHOICES, max_length=10)
    birthday = models.DateField('Дата рождения', null=True)
    phoneNumber = models.CharField('Телефон', unique=True, max_length=20, null=True)
    email = models.EmailField('Email', unique=True)
    country = models.CharField('Страна', choices=settings.COUNTRY_CHOICES, max_length=128)
    city = models.CharField('Город', max_length=128)
    area = models.CharField('Область', max_length=128)
    swPlace = models.CharField('Место работы/учёбы', max_length=128, blank=True)
    balance = models.FloatField('Баланс', default=0.00)

    # team
    team_role = models.CharField('Роль в команде', choices=settings.TEAM_ROLES, max_length=10, null=True, blank=True)
    number_in_the_team = models.CharField(
        'Номер в команде', choices=settings.TEAM_NUMBERS, max_length=1, null=True, blank=True)

    # toggles
    is_staff = models.BooleanField('Персонал', default=False)
    is_active = models.BooleanField('Активация аккаунта', default=False)
    hide_my_name = models.BooleanField('Скрыть имя и фамилию', default=False)

    # rating
    author_rating = models.IntegerField('Рейтинг автора', default=0)
    rating = models.IntegerField('Рейтинг', default=0)
    league = models.CharField('Лига', choices=(
        ('l1', 'Школьная лига'), ('l2', 'Лига колледжей'), ('l3', 'Студенческая лига'),
        ('l4', 'Высшая лига'), ('l5', 'Премьер-лига'), ('l6', 'Супер-лига')),
                              blank=True, max_length=128)

    date_joined = models.DateTimeField('Дата регистрации', default=timezone.now)
    last_game = models.DateTimeField('Дата последней игры', default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')


