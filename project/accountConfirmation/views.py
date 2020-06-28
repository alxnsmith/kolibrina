from django.shortcuts import render, HttpResponse
from base64 import b64decode
from userK.models import CustomUser as User


def confirmAccount(request):
    try:
        e = b64decode(bytes(request.GET.get('c'), 'utf-8').decode('utf-8'))
        p = str(e.decode('utf-8'))
        u = User.objects.get(email=p)
        if not u.is_active:
            u.is_active = True
            u.save()
            return HttpResponse("Good, lucky game!")
        else:
            return HttpResponse('Ссылка не действительна!')
    except:
        return HttpResponse('Ссылка не действительна!')
