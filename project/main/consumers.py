from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import TextInfo


class TextInfoConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.game_type = self.scope['url_route']['kwargs']['game_type']
        await self.accept()
        await self.send_text_info()

    async def send_text_info(self):
        text_info = await database_sync_to_async(self.get_text_info)()
        if text_info:
            await self.send_json({'type': 'text_info', 'text_info': text_info})

    def get_text_info(self):
        if (query_set := TextInfo.objects.all()).exists():
            text_info_instance = query_set.last()
            if self.game_type == 'train':
                return text_info_instance.train
            elif self.game_type == 'tournament_week':
                return text_info_instance.tournament_week
            elif self.game_type == 'marathon_week_official':
                return text_info_instance.marathon_week_official
        else:
            return None
