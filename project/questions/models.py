from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from userK.models import User


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

    purpose = models.ForeignKey(Purpose, on_delete=models.SET_NULL, db_column='purpose', default=None,
                                verbose_name='Назначение', null=True, blank=True)
    premoderate = models.BooleanField(default=True, verbose_name='На модерации')
    pos = models.CharField(choices=posChoices, max_length=10, verbose_name='Позиция вопроса в турнире', blank=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='author', verbose_name='Автор',
                               default=None, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, default='0', db_column='category', null=True,
                                 verbose_name='Категория')
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, default='0', db_column='theme', verbose_name='Тема',
                              null=True)
    difficulty = models.CharField(choices=diffChoices, max_length=2, default='30', verbose_name='Сложность')
    question = models.TextField(max_length=350, verbose_name='Вопрос')
    correct_answer = models.CharField(max_length=64, verbose_name='Правильный ответ')
    answer2 = models.CharField(max_length=64, verbose_name='Ответ2')
    answer3 = models.CharField(max_length=64, verbose_name='Ответ3')
    answer4 = models.CharField(max_length=64, verbose_name='Ответ4')

    def __str__(self):
        # if len(self.question) > 50:
        # question_str = self.question[:50] + '...'
        # else:
        #     question_str = self.question.ljust(50, '_')
        return 'M: {}, ID: {}, Q: {}, A: {}, D: {}, C: {}, T: {}'.format(self.premoderate,
                                                                         self.id,
                                                                         self.question,
                                                                         self.correct_answer,
                                                                         self.difficulty,
                                                                         self.category,
                                                                         self.theme)

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')


class Tournament(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя турнира', blank=True)

    class Purposes(models.TextChoices):
        NONE = 'NONE', _('Не указано')
        TRAIN_ER_LOTTO = 'TEL', _('Тренировка эрудит-лото')
        TOURNAMENT_WEEK_ER_LOTTO = 'TWEL', _('Турнир недели эрудит-лото')

    purposes = models.CharField(verbose_name='Назначение', max_length=128, choices=Purposes.choices,
                                default=Purposes.NONE)
    author = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL,
                               verbose_name="Автор турнира")
    timer = models.IntegerField(verbose_name='Время таймера', default=30)
    date = models.DateTimeField(verbose_name='Дата и время проведения', blank=True, null=True)
    create_date = models.DateField(verbose_name='Дата создания', default=timezone.now)
    is_active = models.BooleanField(verbose_name="Активный турнир", default=False)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return f'Name: {self.name}; Author: {self.author}; Create date: {self.create_date}'

    class Meta:
        verbose_name = _('Турнир')
        verbose_name_plural = _('Турниры')


class Attempt(models.Model):
    class Attempts(models.IntegerChoices):
        ONE = 1, _('Одна')
        TWO = 2, _('Две')
        THREE = 3, _('Три')

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name='Турнир')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Игрок')
    attempt = models.IntegerField(verbose_name='Попыток совершено', choices=Attempts.choices, default=Attempts.ONE)
    lose_num_question = models.IntegerField(verbose_name='Номер, последнего вопроса', default=0)
    attempt2 = models.BooleanField(verbose_name='Разрешить вторую попытку', default=False)
    attempt3 = models.BooleanField(verbose_name='Разрешить третью попытку', default=False)

    def __str__(self):
        return f'T: {self.tournament}; P: {self.user}, A: {self.attempt}'

    class Meta:
        verbose_name = _('Попытка')
        verbose_name_plural = _('Попытки')


class MarafonThemeBlock(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return f'Theme: {self.theme}; Author: {self.author};'

    class Meta:
        verbose_name = _('Блок темы')
        verbose_name_plural = _('Блоки тем')


class Marafon(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя марафона', blank=True)

    class Purposes(models.TextChoices):
        NONE = 'NONE', _('Не указано')
        MARAFON_WEEK_ER_LOTTO = 'MWEL', _('Марафон недели эрудит-лото')

    purpose = models.CharField(verbose_name='Назначение', max_length=128, choices=Purposes.choices,
                               default=Purposes.NONE)
    author = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL,
                               verbose_name="Автор марафона")
    question_blocks = models.ManyToManyField(MarafonThemeBlock)
    timer = models.IntegerField(verbose_name='Время таймера', default=30)
    date = models.DateTimeField(verbose_name='Дата и время проведения', blank=True, null=True)
    create_date = models.DateField(verbose_name='Дата создания', default=timezone.now)
    is_active = models.BooleanField(verbose_name="Активный марафон", default=False)

    def __str__(self):
        return f'A: {self.is_active};Name: {self.name}; Author: {self.author}; Create date: {self.create_date}'

    class Meta:
        verbose_name = _('Марафоны')
        verbose_name_plural = _('Марафоны')
