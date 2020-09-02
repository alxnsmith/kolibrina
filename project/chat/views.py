from django.shortcuts import render, redirect
from media.models import Banner


def chat(request):
    if request.user.is_authenticated:
        if Banner.objects.filter(name='MainBanner').exists():
            mainBanner = str(Banner.objects.filter(name='MainBanner')[0].image)
        else:
            mainBanner = False
        return render(request, 'chat/chat.html', {
            'mainBanner': mainBanner,
        })
    else:
        return redirect('login')