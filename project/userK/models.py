from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.conf import settings

from stats.services import get_sum_score_user, init_league

from media.models import Avatar
from api_teams.models import Team

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # personal data
    username = models.CharField(verbose_name='Никнейм', unique=True, max_length=30)
    firstName = models.CharField(verbose_name='Имя', max_length=128)
    lastName = models.CharField(verbose_name='Фамилия', max_length=128)
    gender = models.CharField(verbose_name='Пол', choices=settings.GENDER_CHOICES, max_length=10)
    birthday = models.DateField(verbose_name='Дата рождения', null=True)
    phoneNumber = models.CharField(verbose_name='Телефон', unique=True, max_length=20, null=True)
    email = models.EmailField(verbose_name='Email', unique=True)
    country = models.CharField(verbose_name='Страна', choices=settings.COUNTRY_CHOICES, max_length=128)
    city = models.CharField(verbose_name='Город', max_length=128)
    area = models.CharField(verbose_name='Область', max_length=128)
    swPlace = models.CharField(
        verbose_name='Место работы / учёбы: ВУЗ / колледж / школа - класс', max_length=128, blank=True)
    balance = models.FloatField(verbose_name='Баланс', default=0.00)

    # team
    team = models.ForeignKey(Team, verbose_name='Команда', on_delete=models.SET_NULL, blank=True, null=True)
    team_role = models.CharField(
        verbose_name='Роль в команде', choices=settings.TEAM_ROLES, max_length=10, null=True, blank=True)
    number_in_the_team = models.CharField(
        verbose_name='Номер в команде', choices=settings.TEAM_NUMBERS, max_length=1, null=True, blank=True)

    # toggles
    is_staff = models.BooleanField(verbose_name='Администратор', default=False)
    is_free_member = models.BooleanField(verbose_name='Льготник', default=False)
    is_active = models.BooleanField(verbose_name='Активация аккаунта', default=False)
    hideMyName = models.BooleanField(verbose_name='Скрыть имя и фамилию', default=False)

    # rating
    rating = models.CharField(verbose_name='Опыт(Очки уровня)', default=0, max_length=128)
    league = models.CharField(verbose_name='Лига', choices=(
        ('l1', 'Школьная лига'), ('l2', 'Лига колледжей'), ('l3', 'Студенческая лига'),
        ('l4', 'Высшая лига'), ('l5', 'Премьер-лига'), ('l6', 'Супер-лига')),
                              blank=True, max_length=128)

    # Parents and childs
    parent_account_id = models.CharField(verbose_name='Родительский аккаунт', default='', max_length=20, blank=True)
    child_account = models.BooleanField(verbose_name='Детский аккаунт', default=False)

    # Hint stat
    countHintMaster = models.CharField(verbose_name='Счетчик подсказок мастера', default=0, max_length=128)
    countHintDelTwoAnswer = models.CharField(verbose_name='Счетчик подсказок "Убрать два ответа"', default=0,
                                             max_length=128)
    countHintChance = models.CharField(verbose_name='Счетчик подсказок "Второй шанс"', default=0, max_length=128)
    countHintSkipQuest = models.CharField(verbose_name='Счетчик пропуска вопроса', default=0, max_length=128)
    # Answers stat
    countRightAnswer = models.CharField(verbose_name='Счетчик правильных ответов', default=0, max_length=128)
    countWrongAnswer = models.CharField(verbose_name='Счетчик неправильныых ответов', default=0, max_length=128)
    countTotalGames = models.CharField(verbose_name='Счетчик игр', default=0, max_length=128)

    date_joined = models.DateTimeField(verbose_name='Дата регистрации', default=timezone.now)
    last_game = models.DateTimeField(verbose_name='Дата последней игры', default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.rating = get_sum_score_user(self)
        init_league(self)
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class InviteToTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'"{self.user}" invited to "{self.team}"'
