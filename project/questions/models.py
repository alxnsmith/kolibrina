from django.db import models
from userK.models import CustomUser
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Tournament(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя турнира', blank=True)

    class Destinations(models.TextChoices):
        NONE = 'NONE', _('Не указано')
        TRAIN_ER_LOTTO = 'TEL', _('Тренировка эрудит-лото')
        TOURNAMENT_WEEK_ER_LOTTO = 'TWEL', _('Турнир недели эрудит-лото')
    destination = models.CharField(verbose_name='Назначение', max_length=128, choices=Destinations.choices, default=Destinations.NONE)
    author = models.ForeignKey(CustomUser, default=None, null=True, on_delete=models.SET_NULL, verbose_name="Автор турнира")
    timer = models.IntegerField(verbose_name='Время таймера', default=30)
    date = models.DateTimeField(verbose_name='Дата и время проведения', blank=True, null=True)
    create_date = models.DateField(verbose_name='Дата создания', default=timezone.now)
    is_active = models.BooleanField(verbose_name="Активный турнир", default=False)

    def __str__(self):
        return f'Name: {self.name}; Author: {self.author}; Create date: {self.create_date}'


class Category(models.Model):
    category = models.CharField(max_length=25, verbose_name='Категория')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class Purpose(models.Model):
    purpose = models.CharField(max_length=150, verbose_name='Назначение')

    def __str__(self):
        return self.purpose

    class Meta:
        verbose_name = _('Назначение')
        verbose_name_plural = _('Назначения')


class Theme(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default='0', db_column='category',
                                 verbose_name='Категория')
    theme = models.CharField(max_length=50, verbose_name='Тема')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = _('Тема')
        verbose_name_plural = _('Темы')


class Question(models.Model):
    diffChoices = (('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'))
    posChoices = (
        ('1', '01'), ('2', '02'), ('3', '03'), ('4', '04'), ('5', '05'), ('6', '06'),
        ('7', '07'), ('8', '08'), ('9', '09'), ('10', '10'), ('11', '11'), ('12', '12'),
        ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'),
        ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'),
        ('25', '25'), ('d1.1', 'д1.1'), ('d1.2', 'д1.2'), ('d1.3', 'д1.3'), ('d1.4', 'д1.4'), ('d1.5', 'д1.5'),
        ('d2.1', 'д2.1'), ('d2.2', 'д2.2'), ('d2.3', 'д2.3'), ('d2.4', 'д2.4'), ('d2.5', 'д2.5'), ('zamena', 'замена'),
    )

    purpose = models.ForeignKey(Purpose, on_delete=models.SET_NULL, db_column='purpose', default=None,
                                verbose_name='Назначение', null=True, blank=True)
    premoderate = models.BooleanField(default=True, verbose_name='На модерации')
    for_tournament = models.ForeignKey(Tournament, default=None, on_delete=models.SET_NULL, verbose_name='Для турнира', null=True, blank=True)
    pos = models.CharField(choices=posChoices, max_length=10, verbose_name='Позиция вопроса в турнире', blank=True)

    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, db_column='author', verbose_name='Автор',
                               default=None, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default='0', db_column='category',
                                 verbose_name='Категория')
    theme = models.ForeignKey(Theme, on_delete=models.DO_NOTHING, default='0', db_column='theme', verbose_name='Тема')
    difficulty = models.CharField(choices=diffChoices, max_length=2, default='30', verbose_name='Сложность')
    question = models.TextField(max_length=350, verbose_name='Вопрос')
    correct_answer = models.CharField(max_length=64, verbose_name='Правильный ответ')
    answer2 = models.CharField(max_length=64, verbose_name='Ответ2')
    answer3 = models.CharField(max_length=64, verbose_name='Ответ3')
    answer4 = models.CharField(max_length=64, verbose_name='Ответ4')

    def __str__(self):
        if len(self.question) > 50:
            question_str = self.question[:50] + '...'
        else:
            question_str = self.question.ljust(50, '_')
        return 'ID: {}, Q: {}, A: {}, D: {}, C: {}, T: {}'.format(self.id,
                                                                     question_str,
                                                                     self.correct_answer,
                                                                     self.difficulty,
                                                                     self.category,
                                                                     self.theme)

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')

