from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class OnlineConsumer(WebsocketConsumer):
    online_list = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = self.scope['user']

    def connect(self):
        self.username = str(self.username)
        async_to_sync(self.channel_layer.group_add)(
            'online',
            self.channel_name
        )
        self.accept()
        if self.online_list.get(self.username):
            self.online_list[self.username] += 1
        elif self.username != 'AnonymousUser':
            self.online_list[self.username] = 1
        self.send_online()

    def disconnect(self, code):
        if self.username != 'AnonymousUser':
            self.send_online()
            if self.online_list.get(self.username):
                self.online_list[self.username] -= 1
                if self.online_list[self.username] == 0:
                    del self.online_list[self.username]

    def new_online(self, event):
        value = event['value']
        self.send(value)

    def send_online(self):
        async_to_sync(self.channel_layer.group_send)(
            'online',
            {'type': 'new_online',
             'value': str(len(self.online_list))}
        )