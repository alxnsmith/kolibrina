from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from userK.services import activate_user
from .forms import RegistrationForm
from .services import do_register, create_render_data, write_user_model


class Account(View):
    def get(self, request):
        return render(request, 'userK/account.html', self.render_data)

    def post(self, request):
        post = request.POST
        if post.get('type') == 'user_info':
            data = create_render_data(request)
            result = write_user_model(request.user, request.POST)
            if result['status'] == 'OK':
                return redirect('account')
            elif result['status'] == 'error':
                error = {'error': result['error']}
                data['errors'].append(error)
        elif post.get('type') == 'avatar':
            user_model = request.user
            if avatar := request.FILES.get('image'):
                user_model.avatar = avatar
                user_model.save()
        return render(request, 'userK/account.html', self.render_data)

    @property
    def render_data(self):
        return create_render_data(self.request)


class Register(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('account')
        form = RegistrationForm()
        return render(request, 'userK/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, 'userK/register.html', {'form': form})
        data = form.cleaned_data
        do_register(username=data.get('username'), email=data.get('email'), birthday=data.get('birthday'),
                    password=data.get('password1'))

        return HttpResponse('Успешная регистрация!<br>'
                            'На указанный адрес электронной почты была отправлена ссылка для подтверждения аккаунта.')


class ConfirmAccount(View):
    def get(self, request):
        try:
            get = request.GET
            code_activation = get.get('c')
            activate_user(code_activation)

            logout(request)
            msg = 'Отлично!<br>' \
                  'Вы только что активировали аккаунт!<br>' \
                  f'Теперь вы можете перейти на <a href="{reverse("login")}">страницу авторизации</a> и войти в свой аккаунт'
            return HttpResponse(msg)

        except Exception as exc:
            return HttpResponse(f'Ссылка не действительна! {exc}')
