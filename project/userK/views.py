from django.shortcuts import render, redirect


def account(request):
    if request.user.is_authenticated:
        id = str(request.user.id).rjust(7, '0')
        return render(request, 'userK/account.html', {'id': id})
    else:
        return redirect('login')