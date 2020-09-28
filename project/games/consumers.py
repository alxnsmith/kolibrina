import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

from questions.models import Tournament
from questions.services import get_questions_from_tournament
import redis
from django.conf import settings


class TournamentWeek(WebsocketConsumer):
    questions_queryset: object
    tournament_model: Tournament
    tournament_shortname: str

    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)

    def connect(self):
        self.tournament_shortname = self.scope['url_route']['kwargs']['tournament_name']
        self.tournament_model = self._get_tournament_model()
        self.questions_queryset = get_questions_from_tournament(self.tournament_model)
        async_to_sync(self.channel_layer.group_add)(
            self.tournament_shortname,
            self.channel_name
        )
        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.tournament_shortname,
            {'type': 'send_timer_duration',
             'timer': self.tournament_model.timer})

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.tournament_shortname,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        if 'event' in text_data:
            print(self._gen_question().pos)

    def send_timer_duration(self, event):
        self.send(text_data=json.dumps(event))

    def _get_tournament_model(self):
        date_range = (timezone.now() - timezone.timedelta(days=7), timezone.now())  # last 7 days
        active_tournaments_list = Tournament.objects.filter(
            is_active=True, destination=self.tournament_shortname,
            date__range=date_range)
        tournament_model = active_tournaments_list.order_by('date')[0]
        return tournament_model

    def _gen_question(self):
        return self.questions_queryset.get(pos='1')