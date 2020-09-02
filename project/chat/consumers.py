import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import redis
from django.conf import settings



class ChatConsumer(WebsocketConsumer):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)
    redis_instance.set('ChatOnline', '0')

    def connect(self):
        self.redis_instance.set('ChatOnline', str(int(self.redis_instance.get('ChatOnline'))+1))
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
        self.redis_instance.set('ChatOnline', str(int(self.redis_instance.get('ChatOnline'))-1))
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        """Receive message from WebSocket"""
        text_data_json = json.loads(text_data)
        message = {'message': text_data_json['message'],
                   'username': text_data_json['username']}

        self._mesage_buffer(message=message)  # save last 20 messages

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type': 'chat_message',
             'message': message})

    def chat_message(self, event):
        """Receive message from room group"""

        message = event['message']['message']
        username = event['message']['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'online': int(self.redis_instance.get('ChatOnline')),
            'message_list': self.redis_instance.get(f'{self.room_group_name}_messages').decode(),
        }))


    def _mesage_buffer(self, message):
        if self.redis_instance.exists(f'{self.room_group_name}_messages') == 1:
            message_list = json.loads(self.redis_instance.get(f'{self.room_group_name}_messages').decode())
            message_list.append(message)
            if len(message_list) <= 20:
                self.redis_instance.set(f'{self.room_group_name}_messages',
                                        json.dumps(message_list))
            else:
                message_list = message_list[1:]
                self.redis_instance.set(f'{self.room_group_name}_messages',
                                        json.dumps(message_list))
        else:
            self.redis_instance.set(f'{self.room_group_name}_messages', json.dumps([message]))