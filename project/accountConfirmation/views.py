from django.shortcuts import HttpResponse
from django.urls import reverse
from django.contrib.auth import logout

from userK.models import ConfirmKey
from main.sendmail import sendmail_admins
from userK.services import activate_user


def confirmAccount(request):
    try:
        get = request.GET
        key_object = ConfirmKey.objects.get(code=get.get('c'))
        user = key_object.user
        activate_user(key_object)

        logout(request)
        message = 'Новый пользователь прошел активацию!\n'\
                  f'id: {user.id}\n' \
                  f'username: {user.username}\n' \
                  f'email: {user.email}'
        sendmail_admins('Новая регистрация', message)

        msg = 'Отлично!<br>'\
              'Вы только что активировали аккаунт!<br>'\
              f'Теперь вы можете перейти на <a href="{reverse("login")}">страницу авторизации</a> и войти в свой аккаунт'
        return HttpResponse(msg)

    except Exception as exc:
        return HttpResponse(f'Ссылка не действительна! {exc}')
