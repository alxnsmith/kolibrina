import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import redis
from django.conf import settings


class OnlineConsumer(WebsocketConsumer):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=0)

    def connect(self):
        self.room_group_name = 'online'
        self.username = str(self.scope['user'])

        #  Join to room
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.redis_instance.zincrby(self.room_group_name, 1, self.username)

        self._update_online()

    def disconnect(self, code):
        #  Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        self.redis_instance.zincrby(self.room_group_name, -1, self.username)
        if self.redis_instance.zscore(self.room_group_name, self.username) < 1:
            self.redis_instance.zrem(self.room_group_name, self.username)

        self._update_online()

    def send_online(self, event):
        online = event['online']

        self.send(text_data=json.dumps(
            {
                'type': 'online',
                'online': online
            }))

    def _update_online(self):
        online = self.redis_instance.zcard(self.room_group_name)
        if b'AnonymousUser' in self.redis_instance.zrange(self.room_group_name, 0, -1):
            online = online - 1 + self.redis_instance.zscore(self.room_group_name, 'AnonymousUser')

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type': 'send_online',
             'online': online}
        )
