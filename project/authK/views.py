from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from userK.models import User as User
from django.shortcuts import HttpResponse


def loginK(request):
    if not request.user.is_authenticated:
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('account')
                    # Redirect to a success page.
                else:
                    return render(request, 'loginK/login.html',
                                  {'errTXT': 'Введите имя пользователя'})
            else:
                if request.user == 'AnonymousUser':
                    if not User.objects.filter(username=username)[0].is_active:
                        return render(request, 'loginK/login.html',
                                      {'errors': ['Ваш аккаунт не активирован, проверьте почту.',
                                                 'После регистрации вам на почту была выслана ссылка на активацию аккаунта']})
                    else:
                        return render(request, 'loginK/login.html', {'errors': ['С вашим аккаунтом что-то не так,'
                                                                               'обратитесь в техподдержку.']})
                else:
                    return render(request, 'loginK/login.html', {'errors': ['Неверный логин или пароль']})
        else:
            return render(request, 'loginK/login.html', {'hide': 'hide'})
    else:
        return redirect('account')


def logoutK(request):
    logout(request)
    return redirect('login')
