from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import redis
from django.conf import settings


class ChatConsumer(AsyncJsonWebsocketConsumer):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=settings.REDIS_DB)
    redis_instance.set('ChatOnline', '0')

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.messages_redis_key = f'{self.room_group_name}_messages'
        self.redis_instance.incr('ChatOnline')

        await self.accept()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_online',
                'online': int(self.redis_instance.get('ChatOnline'))
            }
        )

        if history := self.redis_instance.lrange(self.messages_redis_key, 0, -1):  # get all messages
            for mes in history:
                mes = await self.decode_json(mes)
                message = {'type': 'message',
                           'message': mes['message'],
                           'username': mes['username'],
                           'time': mes['time']}
                await self.send_json(message)

    async def disconnect(self, code):
        self.redis_instance.decr('ChatOnline')
        await self.channel_layer.group_discard(  # Leave room group
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_online',
             'online': self.redis_instance.get('ChatOnline').decode()}
        )

    async def receive_json(self, content, **kwargs):
        """Receive message from WebSocket"""
        message = {
            'type': 'message',
            'message': content['message'],
            'time': content['time'],
            'username': str(self.scope['user'])
        }
        self._message_buffer(message=await self.encode_json(message))

        await self.channel_layer.group_send(  # Send message to room group
            self.room_group_name,
            {'type': 'chat_message', 'message': message})

    async def chat_message(self, event):
        message = event['message']
        await self.send_json({**message})

    async def chat_online(self, event):
        online = event['online']
        await self.send_json({
            'type': 'online',
            'online': online,
        })

    def _message_buffer(self, message: str):
        if self.redis_instance.exists(self.messages_redis_key) == 1:
            self.redis_instance.ltrim(self.messages_redis_key, -20, -1)  # trim to last 20 messages
        self.redis_instance.rpush(self.messages_redis_key, message)
