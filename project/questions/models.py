from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from userK.models import User
from django.conf import settings


class Category(models.Model):
    category = models.CharField(max_length=25, verbose_name='Категория')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class Purpose(models.Model):

    class Purposes(models.TextChoices):
        Train = 'T', _('Тренировка')
        MarathonWeek = 'CELMW', _('Пользовательский Марафон недели')
        OfficialMarathonWeek = 'OELMW', _('Официальный марафон недели')
        TournamentWeek = 'ELTW', _('Турнир недели')

    codename = models.CharField(
        choices=Purposes.choices, max_length=150, verbose_name="Назначение", null=True)

    def __str__(self):
        return self.get_codename_display()

    class Meta:
        verbose_name = _('Назначение')
        verbose_name_plural = _('Назначения')


class Theme(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, default='0', db_column='category',
                                 verbose_name='Категория', null=True)
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

    purpose = models.ForeignKey(Purpose, on_delete=models.SET_NULL, verbose_name='Назначение', null=True, blank=True)
    public = models.BooleanField(default=False, verbose_name='Публичный')
    moderate = models.BooleanField(default=True, verbose_name='На модерации')
    pos = models.CharField(choices=posChoices, max_length=10, verbose_name='Позиция вопроса в турнире', blank=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='author', verbose_name='Автор', null=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, db_column='theme', verbose_name='Тема', null=True)
    difficulty = models.CharField(choices=diffChoices, max_length=2, verbose_name='Сложность', default='10')

    question = models.TextField(max_length=350, verbose_name='Вопрос')
    correct_answer = models.CharField(max_length=64, verbose_name='Правильный ответ')
    answer2 = models.CharField(max_length=64, verbose_name='Ответ2')
    answer3 = models.CharField(max_length=64, verbose_name='Ответ3')
    answer4 = models.CharField(max_length=64, verbose_name='Ответ4')

    rate = models.IntegerField('Оценка', default=0)

    create_date = models.DateTimeField('Дата создания', default=timezone.now)

    def __str__(self):
        return 'M: {}, ID: {}, Q: {}, A: {}, D: {}, C: {}, T: {}'.format(self.moderate,
                                                                         self.id,
                                                                         self.question,
                                                                         self.correct_answer,
                                                                         self.difficulty,
                                                                         self.theme.category,
                                                                         self.theme)

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')
        ordering = ['-create_date']


class MarathonThemeBlock(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)
    public = models.BooleanField(default=False, verbose_name='Публичный')
    questions = models.ManyToManyField(Question)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'ID: {self.id};Theme: {self.theme}; Author: {self.author};'

    class Meta:
        verbose_name = _('Блок темы')
        verbose_name_plural = _('Блоки тем')


def get_all_nearest_events_dict():
    events = {
        'official_marathon': ''
    }
    return events
