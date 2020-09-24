from django.shortcuts import render, redirect
from . import forms, services
from .models import Category, Theme
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json


@login_required(login_url='login')
def navigate(request):
    return render(request, 'questions/questions.html')


@csrf_exempt
def questions_api(request):  # url: questions_api
    user = request.user

    if request.method == 'GET':
        get = request.GET
        if get.__contains__('event'):
            event = get['event']
            if event == 'get_themes_in_category':
                if not get.__contains__('cat'):
                    return JsonResponse({'status': 'error', 'error': 'Error! Need "cat"'})
                cat = Theme.objects.filter(category=get['cat'])
                themes = [[str(i), str(i.id)] for i in cat]
                return JsonResponse({'status': 'OK', 'themes': themes})
            else:
                return JsonResponse({'status': 'error', 'error': 'Error! Unknown event.'})
        else:
            return JsonResponse({'status': 'error', 'error': 'ERROR! Need "event".'})

    elif request.method == 'POST':
        post = json.loads(request.body)
        if post.__contains__('event'):
            event = post['event']
            if event == 'add_theme_to_category':
                if not post.__contains__('cat'):
                    return JsonResponse({'status': 'error', 'error': 'Error! Need "cat"'})
                if not post.__contains__('theme'):
                    return JsonResponse({'status': 'error', 'error': 'Error! Need "theme"'})
                result = services.add_theme_to_category(post)
                if result['status'] == 'OK':
                    return JsonResponse({'status': 'OK', 'result': result})
                else:
                    return JsonResponse({'status': 'error', 'error': result})
            if event == 'add_tournament':
                if not post.__contains__('tournament'):
                    return JsonResponse({'status': 'error', 'error': 'Error! Need "tournament"'})
                result = services.add_tournament(post)
                return JsonResponse(result)
            else:
                return JsonResponse({'status': 'error', 'error': 'Error! Unknown event.'})
        else:
            return JsonResponse({'status': 'error', 'error': 'ERROR! Need "event".'})

    # elif request.method == 'DELETE':
    #     delete = json.loads(request.body)
    #     if delete.__contains__('event'):
    #         event = delete['event']
    #         if event == 'add_player_to_invite_list':
    #             pass
    #         else:
    #             return JsonResponse({'status': 'error', 'error': 'Error! Unknown event.'})
    #     else:
    #         return JsonResponse({'status': 'error', 'error': 'ERROR! Need "event".'})

    # elif request.method == 'PUT':
    #     delete = json.loads(request.body)
    #     if delete.__contains__('event'):
    #         event = delete['event']
    #         if event == 'add_player_to_invite_list':
    #             pass
    #         else:
    #             return JsonResponse({'status': 'error', 'error': 'Error! Unknown event.'})
    #     else:
    #         return JsonResponse({'status': 'error', 'error': 'ERROR! Need "event".'})


def add_tournament_week(request):
    data = {'categories': Category.objects.all()}
    return render(request, 'questions/add-tournament.html', data)


@login_required(login_url='login')
def addQuestion(request):
    if request.user.firstName and request.user.lastName and request.user.city:
        if request.POST:
            services.add_question(post=request.POST)
            print(request.POST)
            return redirect('add-question')
        else:
            data = {
                'form': forms.AddQuestionForm(initial={'author': request.user.id}),
                'categories': Category.objects.all(),
            }
            return render(request, 'questions/add-question.html', data)
    else:
        return render(request, 'questions/add-question.html',
                      {'errors': [
                          {'link': '/account',
                           'tlink': 'Заполните',
                           'error': ' свой профиль для полноценного пользования сервисом.'}]})
