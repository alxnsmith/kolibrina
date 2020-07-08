from django.shortcuts import render, redirect, HttpResponse
from . import forms
from .models import Category, Theme

def getThemes(request):
    x = Theme.objects.filter(category=request._post['x'])
    themes = []
    for i in x:
        themes.append(str(i) + '/|\\' + str(i.id) + '\\|/')
    if request.POST:
        return HttpResponse(themes)
    else:
        # return HttpResponse(', '.join(x.__dict__))
        return redirect('account')


def addQuestion(request):
    if request.user.is_authenticated and request.user.firstName and request.user.lastName and request.user.city:
        if request.POST:
            form = forms.AddQuestionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('add-question')
        else:
            data = {
                'USER': ','.join((request.user.firstName.upper(), request.user.lastName.upper(), request.user.city.upper(),
                                  request.user.email)), 'form': forms.AddQuestionForm(initial={'author': request.user.id, }), 'categories': Category.objects.all(),
            }
            return render(request, 'addquestion/add-question.html', data)
    elif not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'addquestion/add-question.html',
                      {'errors': [
                          {'error': ' свой профиль для полноценного пользования сервисом.', 'link': '/account',
                           'tlink': 'Заполните'},
                      ]})
