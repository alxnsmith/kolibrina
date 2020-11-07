from django.shortcuts import render, redirect
from . import services


def account(request):
    if request.user.is_authenticated:
        data = services.create_render_data(request)
        if request.POST:
            result = services.write_user_model(request.user, request.POST)
            if result['status'] == 'OK':
                return redirect('account')
            elif result['status'] == 'error':
                error = {'error': result['error']}
                data['errors'].append(error)
                return render(request, 'userK/account.html', data)
        else:
            return render(request, 'userK/account.html', data)
    else:
        return redirect('login')
