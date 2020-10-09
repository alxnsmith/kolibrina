import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.services import check_fill_profile
from . import forms, services
from .models import Category, Theme


@login_required(login_url='login')
def navigate(request):
    return render(request, 'questions/questions.html')


@csrf_exempt
def questions_api(request):  # url: questions_api
    if request.method == 'GET':
        get = request.GET
        if 'event' in get:
            event = get['event']
            if event == 'get_themes_in_category':
                if 'cat' not in get:
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
        if 'event' in post:
            event = post['event']
            if event == 'add_theme_to_category':
                if 'cat' not in post:
                    return JsonResponse({'status': 'error', 'error': 'Error! Need "cat"'})
                if 'theme' not in post:
                    return JsonResponse({'status': 'error', 'error': 'Error! Need "theme"'})
                result = services.add_theme_to_category(post)
                if result['status'] == 'OK':
                    return JsonResponse({'status': 'OK', 'result': result})
                else:
                    return JsonResponse({'status': 'error', 'error': result})
            if event == 'add_tournament_week':
                if 'tournament' not in post:
                    return JsonResponse({'status': 'error', 'error': 'Error! Need "tournament"'})
                result = services.add_tournament_week(post)
                return JsonResponse(result)
            else:
                return JsonResponse({'status': 'error', 'error': 'Error! Unknown event.'})
        else:
            return JsonResponse({'status': 'error', 'error': 'ERROR! Need "event".'})

    # elif request.method == 'DELETE':
    #     delete = json.loads(request.body)
    #     if 'event' in delete:
    #         event = delete['event']
    #         if event == 'add_player_to_invite_list':
    #             pass
    #         else:
    #             return JsonResponse({'status': 'error', 'error': 'Error! Unknown event.'})
    #     else:
    #         return JsonResponse({'status': 'error', 'error': 'ERROR! Need "event".'})

    # elif request.method == 'PUT':
    #     delete = json.loads(request.body)
    #     if 'event' in delete:
    #         event = delete['event']
    #         if event == 'add_player_to_invite_list':
    #             pass
    #         else:
    #             return JsonResponse({'status': 'error', 'error': 'Error! Unknown event.'})
    #     else:
    #         return JsonResponse({'status': 'error', 'error': 'ERROR! Need "event".'})


@login_required(login_url='login')
def add_tournament_week(request):
    template = 'questions/add-tournament.html'
    result_check_fill_profile = check_fill_profile(request, template)
    if result_check_fill_profile['status'] == 'error':
        return result_check_fill_profile['response']
    data = {'categories': Category.objects.all()}
    return render(request, template, data)


@login_required(login_url='login')
def add_question(request):
    template = 'questions/add-question.html'
    result_check_fill_profile = check_fill_profile(request, template)
    if result_check_fill_profile['status'] == 'error':
        return result_check_fill_profile['response']
    if request.POST:
        services.add_question(post=request.POST)
        return redirect('add-question')
    else:
        data = {
            'form': forms.AddQuestionForm(initial={'author': request.user.id}),
            'categories': Category.objects.all(),
        }
        return render(request, template, data)


class AddThemeBlocksMarafonWeek(View):
    template_name = 'questions/add-theme-blocks.html'

    def get(self, request):
        q = ''
        for i in request.__dict__:
            q += f'\n\n\n {i} ==== {request.__dict__[i]}'
        data = {
            'qwe': q
        }
        return render(request, self.template_name, data)

