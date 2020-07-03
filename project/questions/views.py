from django.shortcuts import render, redirect, HttpResponse


def navigate(request):
    if request.user.is_authenticated:
        return render(request, 'questions/questions.html')
    else:
        return redirect('login')