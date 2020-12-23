from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer
import redis
from django.conf import settings
from .services import OnlineController


class OnlineConsumer(AsyncJsonWebsocketConsumer):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=settings.REDIS_DB)

    async def connect(self):
        self.room_group_name = 'online'
        self.online_ctrl = OnlineController(self.room_group_name, str(self.scope['user']))

        #  Join to room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        self.online_ctrl.user.connect()
        await self.send_online()

    async def disconnect(self, code):
        #  Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        self.online_ctrl.user.disconnect()

    async def send_online(self, *_):
        await self.send_json({
            'type': 'online', 'online': self.online_ctrl.value
        })
