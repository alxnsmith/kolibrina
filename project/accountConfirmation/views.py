from django.shortcuts import HttpResponse, redirect
from base64 import b64decode
from userK.models import CustomUser as User
from django.conf import settings
from main.sendmail import sendmail


def confirmAccount(request):
    try:
        e = b64decode(bytes(request.GET.get('c'), 'utf-8').decode('utf-8'))
        p = str(e.decode('utf-8'))
        u = User.objects.get(email=p)
        if not u.is_active:
            u.is_active = True
            u.save()
            message = 'Новый пользователь прошел активацию!\n' \
                      f'(id: {u.id}, username: {u.username}, email: {p})'
            sendmail('Новая регистрация', message, settings.EMAIL_ADMIN_USERS)
            return redirect('login')
        else:
            return Exception
    except:
        return HttpResponse('Ссылка не действительна!')
