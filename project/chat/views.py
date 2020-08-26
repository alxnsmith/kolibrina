from django.shortcuts import render, redirect
from media.models import Banner
from django.conf import settings
import redis


def chat(request):
    if request.user.is_authenticated:
        redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                           port=settings.REDIS_PORT, db=0)

        if Banner.objects.filter(name='MainBanner').exists():
            mainBanner = str(Banner.objects.filter(name='MainBanner')[0].image)
        else:
            mainBanner = 'img/banner.png'
        return render(request, 'chat/chat.html', {
            'mainBanner': mainBanner,
            'ChatOnline': redis_instance.get('ChatOnline').decode()
        })
    else:
        return redirect('login')