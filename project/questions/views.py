import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from main.services import check_fill_profile
from . import forms, services
from .models import Category, Theme


@login_required(login_url='login')
def navigate(request):
    return render(request, 'questions/questions.html')


class QuestionAPI(View):
    def get(self, request):
        get = request.GET

        if result := self._exists_in(('event',), get):
            return result

        event = get['event']

        if event == 'get_categories':
            categories = Category.objects.all().values_list('id', 'category')
            categories = [cat for cat in categories]
            return JsonResponse({'status': 'OK', 'categories': categories})
        elif event == 'get_themes_in_category':
            cat = Theme.objects.filter(category=get['cat'])
            themes = [[str(i), str(i.id)] for i in cat]
            return JsonResponse({'status': 'OK', 'themes': themes})
        else:
            return self._status_error('Error! Unknown event.')

    def post(self, request):
        post = json.loads(request.body)
        if result := self._exists_in(('event',), post):
            return result
        event = post['event']
        if event == 'add_question':
            if result := self._exists_in(('cat', 'theme', 'question'), post):
                return result
            result = services.add_theme_to_category(post)
            if result['status'] == 'OK':
                return JsonResponse({'status': 'OK', 'result': result})
            else:
                return self._status_error(result)
        elif event == 'add_theme_to_category':
            if result := self._exists_in(('cat', 'theme'), post):
                return result
            result = services.add_theme_to_category(post)
            if result['status'] == 'OK':
                return JsonResponse({'status': 'OK', 'result': result})
            else:
                return self._status_error(result)
        elif event == 'add_tournament_week':
            if result := self._exists_in(('tournament',), post):
                return result
            result = services.add_tournament_week(post)
            return JsonResponse(result)
        elif event == 'add_marafon_week':
            # if result := self._exists_in(('tournament',), post):
            #     return result
            # result = services.add_tournament_week(post)
            # return JsonResponse(result)
            question_list = post['question_list']
            for i in question_list:
                if str(i).startswith('1'):
                    print(question_list[i])
                if str(i).startswith('2'):
                    print(question_list[i])
                if str(i).startswith('3'):
                    print(question_list[i])
                if str(i).startswith('4'):
                    print(question_list[i])
            return JsonResponse({'status': 'OK'})
        else:
            return self._status_error('Error! Unknown event.')

    @staticmethod
    def _exists_in(keys, checked_element):
        for key in keys:
            if key not in checked_element:
                return self._status_error(f'Error! Need "{key}"')

    @staticmethod
    def _status_error(error):
        return JsonResponse({'status': 'error', 'error': str(error)})


@login_required(login_url='login')
def add_tournament_week(request):
    template = 'questions/add-tournament.html'
    data = {'errors': []}
    if errors := check_fill_profile(request):
        data['errors'] += errors
    return render(request, template, data)


class AddQuestion(View):
    template_name = 'questions/add-question.html'

    def get(self, request):
        data = {'form': forms.AddQuestionForm(initial={'author': request.user.id}), 'errors': []}
        if errors := check_fill_profile(request):
            data['errors'] += errors
        return render(request, self.template_name, data)

    @staticmethod
    def post(request):
        services.add_question(request)
        return redirect('add-question')


class AddThemeBlocksMarafonWeek(View):
    template_name = 'questions/add-themes-blocks.html'

    def get(self, request):
        data = {}
        return render(request, self.template_name, data)
