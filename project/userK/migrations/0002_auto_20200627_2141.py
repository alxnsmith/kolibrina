# Generated by Django 3.0.7 on 2020-06-27 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userK', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Дата рождения'),
        ),
    ]
