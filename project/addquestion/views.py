from django.shortcuts import render, redirect


def addQuestion(request):
    if request.user.is_authenticated and request.user.firstName and request.user.lastName and request.user.city:
        data = {
            'USER': ','.join((request.user.firstName.upper(), request.user.lastName.upper(), request.user.city.upper(),
            request.user.email)),
        }
        return render(request, 'addquestion/add-question.html', data)
    elif not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'addquestion/add-question.html', {'errors': ['Заполните свой профиль для полноценного пользования сервисом.']})
