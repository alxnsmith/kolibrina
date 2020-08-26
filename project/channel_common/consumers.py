import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import redis
from django.conf import settings


class OnlineConsumer(WebsocketConsumer):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)
    redis_instance.set('online', 0)

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'online',
            self.channel_name
        )
        self.redis_instance.set('online', int(self.redis_instance.get('online').decode()) + 1)
        async_to_sync(self.channel_layer.group_send)(
            'online',
            {'type': 'newOnline',
             'value': str(self.redis_instance.get('online').decode())}
        )
        self.accept()
        self.send(self.redis_instance.get('online').decode())

    def disconnect(self, code):
        self.redis_instance.set('online', int(self.redis_instance.get('online').decode())-1)
        async_to_sync(self.channel_layer.group_send)(
            'online',
            {'type': 'newOnline',
             'value': str(self.redis_instance.get('online').decode())}
        )
        self.send(json.dumps({'online': self.redis_instance.get('online').decode()}))

    def newOnline(self, event):
        value = event['value']
        self.send(value)