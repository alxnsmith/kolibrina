from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
import redis
from django.conf import settings


class ChatConsumer(JsonWebsocketConsumer):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=0)
    redis_instance.set('ChatOnline', '0')

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.messages_redis_key = f'{self.room_group_name}_messages'
        self.redis_instance.incr('ChatOnline')

        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_online',
                'online': int(self.redis_instance.get('ChatOnline'))
            }
        )

        if history := self.redis_instance.lrange(self.messages_redis_key, 0, -1):  # get all messages
            for mes in history:
                mes = self.decode_json(mes)
                message = {'type': 'message',
                           'message': mes['message'],
                           'username': mes['username'],
                           'time': mes['time']}
                self.send_json(message)

    def disconnect(self, code):
        self.redis_instance.decr('ChatOnline')
        async_to_sync(self.channel_layer.group_discard)(  # Leave room group
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type': 'chat_online',
             'online': self.redis_instance.get('ChatOnline').decode()}
        )

    def receive_json(self, content, **kwargs):
        """Receive message from WebSocket"""
        message = {
            'type': 'message',
            'message': content['message'],
            'time': content['time'],
            'username': str(self.scope['user'])
        }
        self._message_buffer(message=self.encode_json(message))

        async_to_sync(self.channel_layer.group_send)(  # Send message to room group
            self.room_group_name,
            {'type': 'chat_message', 'message': message})

    def chat_message(self, event):
        message = event['message']
        self.send_json(content={**message})

    def chat_online(self, event):
        online = event['online']
        self.send_json(content={
            'type': 'online',
            'online': online,
        })

    def _message_buffer(self, message: str):
        if self.redis_instance.exists(self.messages_redis_key) == 1:
            self.redis_instance.ltrim(self.messages_redis_key, -20, -1)  # trim to last 20 messages
        self.redis_instance.rpush(self.messages_redis_key, message)
