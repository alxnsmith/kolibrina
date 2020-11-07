from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from userK.models import User


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account')
        return render(request, 'loginK/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        valid = authenticate(username=username, password=password) or False
        user = User.objects.get(username=username) if User.objects.filter(username=username).exists() else None

        if not valid and user is None:
            return render(request, 'loginK/login.html', {'errors': [{'error': 'Неверный логин или пароль'}]})

        if not user.is_active:
            return render(request, 'loginK/login.html',
                          {'errors': [{'error': 'Ваш аккаунт не активирован, проверьте почту. После регистрации '
                                                'вам на почту была выслана ссылка на активацию аккаунта'}]})

        login(request, user)
        next_page = request.GET.get('next') or settings.LOGIN_URL
        return redirect(next_page)


def logoutK(request):
    logout(request)
    return redirect('login')
