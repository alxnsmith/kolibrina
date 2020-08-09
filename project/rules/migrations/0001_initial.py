# Generated by Django 3.1 on 2020-08-09 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderRules', models.CharField(default='', max_length=100, verbose_name='Порядок')),
                ('ruleTitle', models.CharField(default='', max_length=100, verbose_name='Название')),
                ('ruleDescription', models.TextField(default='', verbose_name='Полный текст')),
            ],
            options={
                'verbose_name': 'Правило',
                'verbose_name_plural': 'Правила',
            },
        ),
    ]
