import redis
from celery import shared_task
from django.conf import settings
from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer


@shared_task
def send_online(room):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room,
        {'type': 'send_online'}
    )
    return 'online_sended'
