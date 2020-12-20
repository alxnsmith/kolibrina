from django.db import models


class TextInfo(models.Model):
    train = models.CharField('Тренировка', max_length=200, default='Текстовая информация')
    tournament_week = models.CharField('Тренировка', max_length=200, default='Текстовая информация')
    marathon_week_official = models.CharField(
        'Официальный марафон недели', max_length=200, default='Текстовая информация')
