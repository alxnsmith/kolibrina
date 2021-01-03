from django.shortcuts import HttpResponse, redirect
from base64 import b64decode
from userK.models import User as User
from main.sendmail import sendmail_admins
from django.contrib.auth import logout, login


def confirmAccount(request):
    try:
        encoded_email = b64decode(bytes(request.GET.get('c'), 'utf-8').decode('utf-8'))
        decoded_email = str(encoded_email.decode('utf-8'))
        user = User.objects.get(email=decoded_email)
        if not user.is_active:
            user.is_active = True
            user.save()
            message = 'Новый пользователь прошел активацию!\n' \
                      f'(id: {user.id}, username: {user.username}, email: {decoded_email})'
            sendmail_admins('Новая регистрация', message)
            logout(request)
            # login(request, user)
            return redirect('account')
        else:
            return HttpResponse('User is active!')
    except Exception as exc:
        return HttpResponse(f'Ссылка не действительна! {exc}')
