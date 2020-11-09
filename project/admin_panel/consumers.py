from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
import redis
from django.conf import settings


class OnlineConsumer(JsonWebsocketConsumer):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=settings.REDIS_DB,
                                       charset='utf-8',
                                       decode_responses=True)

    def connect(self):
        self.accept()
        self.send_online()

    def receive_json(self, content, **kwargs):
        print(content)
        if content['event'] == 'get_online':
            self.send_online()

    def send_online(self):
        self.online = self.redis_instance.zrange('online', 0, -1, withscores=True)
        self.send_json({'event': 'online', 'online': self.online})
