import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import redis
from django.conf import settings


class ChatConsumer(WebsocketConsumer):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)
    redis_instance.set('ChatOnline', 0)

    def connect(self):
        self.redis_instance.set('ChatOnline', int(self.redis_instance.get('ChatOnline').decode())+1)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        # Leave room group
        self.redis_instance.set('ChatOnline', int(self.redis_instance.get('ChatOnline').decode())-1)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'online': int(self.redis_instance.get('ChatOnline').decode()),
        }))
