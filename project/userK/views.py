from django.shortcuts import render, redirect
from . import services


def account(request):
    if request.user.is_authenticated:
        data = services.create_render_data(request)
        if request.POST:
            services.write_user_model(request.user, request.POST)
            return redirect('account')
        else:
            return render(request, 'userK/account.html', data)
    else:
        return redirect('login')
