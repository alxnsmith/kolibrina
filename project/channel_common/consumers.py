from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer
import redis
from django.conf import settings


class OnlineConsumer(AsyncJsonWebsocketConsumer):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=settings.REDIS_DB)

    async def connect(self):
        self.room_group_name = 'online'
        self.username = str(self.scope['user'])

        #  Join to room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        self.redis_instance.zincrby(self.room_group_name, 1, self.username)

        await self._update_online()

    async def disconnect(self, code):
        #  Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        self.redis_instance.zincrby(self.room_group_name, -1, self.username)
        if self.redis_instance.zscore(self.room_group_name, self.username) < 1:
            self.redis_instance.zrem(self.room_group_name, self.username)

        await self._update_online()

    async def send_online(self, event):
        online = event['online']

        await self.send_json({
            'type': 'online', 'online': online
        })

    async def _update_online(self):
        online = self.redis_instance.zcard(self.room_group_name)
        if b'AnonymousUser' in self.redis_instance.zrange(self.room_group_name, 0, -1):
            online = online - 1 + self.redis_instance.zscore(self.room_group_name, 'AnonymousUser')

        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'send_online',
             'online': online}
        )
