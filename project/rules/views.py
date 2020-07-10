from django.shortcuts import render
from media.models import Banner


def rules(request):
    if Banner.objects.filter(name='MainBanner').exists():
        mainBanner = str(Banner.objects.filter(name='MainBanner')[0].image)
    else:
        mainBanner = 'img/banner.png'
    return render(request, 'rules/rules.html', {'mainBanner': mainBanner})