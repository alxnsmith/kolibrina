from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from questions.models import Purpose


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = get_user_model()
        admin = user.objects.create_superuser(username='admin', email='admin@kolibrina.ru', password='admin')
        admins = Group.objects.create(name='Admins')
        admin.groups.add(admins)
        benefit_recipients = Group.objects.create(name='Benefit recipients')
        admin.groups.add(benefit_recipients)
        Purpose.objects.create(purpose='Training')
        Purpose.objects.create(purpose='Marafon')
        Purpose.objects.create(purpose='TournamentWeek')
