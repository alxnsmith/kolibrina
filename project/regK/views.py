import json
from base64 import b64encode

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from main.sendmail import sendmail
from userK.models import User


class Register(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('account')
        return render(request, 'regK/register.html')

    def post(self, request):

        post = json.loads(request.body)
        context = {'status': 'ok'}
        errors = []
        username = post.get('username').lower().strip()
        email = post.get('email').lower().strip()
        pass1 = post.get('password1')
        pass2 = post.get('password2')
        if not (username and email and pass1 and pass2):
            errors.append({'error': 'Заполните все необходимые поля и подтвердите согласие.'})
            context['status'] = 'error'
            context['errors'] = errors
            return JsonResponse(context)

        for word in settings.RESERVED_USERNAME_WORDS:
            if word in username:
                errors.append({'error': 'В имени пользователя используются зарезервированые ключевые слова: ' + word,
                               'field_name': 'username'})
        if User.objects.filter(username=username).exists() and not errors:
            errors.append({'error': 'Данное имя пользователя уже занято, попробуйте другое.',
                           'field_name': 'username'})
        elif User.objects.filter(email=email).exists():
            errors.append({'error': 'Данная почта уже занята, попробуйте другую.',
                           'field_name': 'email'})
        elif pass1 != pass2 and not errors:
            errors.append({'error': 'Пароли не совпадают.', 'field_name': 'pass'})
        if errors:
            context['status'] = 'error'
            context['errors'] = errors
        else:
            User.objects.create_user(username=username, email=email, password=pass1)
            confirm_code = b64encode(email.encode('utf-8')).decode("utf-8")
            confirm_url = 'https://' + settings.DOMAIN + r'/accountconfirmation/account/email?c=' + confirm_code
            message_text = f'Ваша ссылка для активации аккаунта: \n {confirm_url}'
            sendmail('Активация аккаунта', message_text, email)
        return JsonResponse(context)
