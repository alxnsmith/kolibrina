from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from questions.models import Purpose


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-d', '--develop', type=int, help='Might be 0 or 1, default=0\n'
                                                              'Adds testing models and other things for develop')

    def handle(self, *args, **options):
        dev = True if options.get('develop') == 1 else False
        if dev:
            from questions.models import Category, Theme
            category = Category.objects.create(category='Программирование')
            print('Added category "Программирование"')
            Theme.objects.create(category=category, theme='Python', is_active=True)
            print('Added theme "Python" top parent category')
            Theme.objects.create(category=category, theme='Java', is_active=True)
            print('Added theme "Java" top parent category')
            Theme.objects.create(category=category, theme='Assembler', is_active=True)
            print('Added theme "Assembler" top parent category')
            category = Category.objects.create(category='История')
            print('Added category "История"')
            Theme.objects.create(category=category, theme='Вторая мировая', is_active=True)
            print('Added theme "Вторая мировая" top parent category')
            Theme.objects.create(category=category, theme='Крепостное право', is_active=True)
            print('Added theme "Крепостное право" top parent category')
            category = Category.objects.create(category='Дизайн')
            print('Added category: "Дизайн"')
            Theme.objects.create(category=category, theme='Тени', is_active=True)
            print('Added theme "Тени" top parent category')
            Theme.objects.create(category=category, theme='Перспектива', is_active=True)
            print('Added theme "Перспектива" top parent category')
            Theme.objects.create(category=category, theme='Photoshop', is_active=True)
            print('Added theme "Photoshop" top parent category')
            Theme.objects.create(category=category, theme='Figma', is_active=True)
            print('Added theme "Figma" top parent category')

        user = get_user_model()
        admin = user.objects.create_superuser(username='admin', email='admin@kolibrina.ru', password='admin')
        admins = Group.objects.create(name='Admins')
        admin.groups.add(admins)

        purposes = [purpose for purpose in Purpose.Purposes]
        for purpose in purposes:
            Purpose.objects.create(codename=purpose)

        print('Success!')
