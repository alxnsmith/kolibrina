import redis
from django.conf import settings
import json
from django.http import JsonResponse


def get_last_messages(request):
    if request.GET.__contains__('mainROOM'):
        room_group_name = 'mainROOM'
        redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                           port=settings.REDIS_PORT, db=0)
        if redis_instance.exists(f'chat_{room_group_name}_messages') == 1:
            message_list = redis_instance.get(f'chat_{room_group_name}_messages').decode()
            return JsonResponse({'message_list': message_list})
    return JsonResponse({'message_list': []})