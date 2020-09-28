from django.shortcuts import render, redirect, Http404
from django.contrib.auth.decorators import login_required
from questions.models import Question, Category, Theme
from userK import services as user_services, models as user_models
from . import defs, services
from main.sendmail import sendmail
from django.conf import settings
from django.http import JsonResponse
from questions.models import Tournament


def api_train(request):
    quest_list = []

    def quest_l(questions_list, index):
        if questions_list[index]:
            for i in questions_list[index]:
                d = i.__dict__
                city = user_models.CustomUser.objects.get(id=d['author_id']).city
                if user_models.CustomUser.objects.get(id=d['author_id']).hideMyName or not city:
                    d['author'] = user_models.CustomUser.objects.get(id=d['author_id']).username
                else:
                    d['author'] = '{0} {1}, г.{2}'.format(
                        user_models.CustomUser.objects.get(id=d['author_id']).firstName,
                        user_models.CustomUser.objects.get(id=d['author_id']).lastName, city,
                    )
                d['category'] = str(Category.objects.get(id=d['category_id']))
                d['theme'] = str(Theme.objects.get(id=d['theme_id']))
                del d['_state'], d['purpose_id'], d['premoderate'], d['author_id'], d['category_id'], d['theme_id'],
                quest_list.append(d)
    if request.GET['games'] == 'train':

        if str(request.user) != 'AnonymousUser':
            league = user_services.get_user_rating_lvl_dif(int(request.user.rating))['level']
        else:
            league = 'Z'
        quest_template = defs.q_template(league)
        questions = defs.q_questions(league, Question)
        questions = {'q10': questions['10'], 'q20': questions['20'], 'q30': questions['30'],
                     'q40': questions['40'], 'q50': questions['50']}
        quest_l(questions, 'q10')
        quest_l(questions, 'q20')
        quest_l(questions, 'q30')
        quest_l(questions, 'q40')
        quest_l(questions, 'q50')

        response = {'quest_list': quest_list, 'league': league, 'quest_template': quest_template}
        return JsonResponse(response, safe=False)


def tournaments(request):
    return render(request, 'game/tournaments.html')


def train(request):
    raw_data = services.create_render_data_for_train_el(request)
    if raw_data['status'] == 'error':
        raise Http404(raw_data['error'])
    del raw_data['status']
    data = raw_data
    return render(request, 'game/train.html', data)


@login_required(login_url='login')
def tournament_week(request):
    raw_data = services.create_render_data_for_tournament_week_el(request)
    if raw_data['status'] == 'error':
        raise Http404(raw_data['error'])
    del raw_data['status']
    data = raw_data
    return render(request, 'game/er-loto.html', data)


@login_required(login_url='login')
def win_lose(request):
    if 'status' in request.GET:
        status = request.GET['status']
        score = request.GET["score"]
        if status == 'lose':
            author = f'{request.GET["author"]}'
            question = f'{request.GET["question"]}'
            correct_answer = f'{request.GET["correctAnswer"]}'
            score = f'<span>{score} баллов</span>'
            new_game = f'{request.GET["newGame"]}'
            quest_id = f'{request.GET["questID"]}'
            return render(request, 'game/win-lose/wrong.html', {'question': question, 'correctAnswer': correct_answer,
                                                                'score': score, 'author': author, 'newGame': new_game,
                                                                'questID': quest_id})
        elif status == 'win':
            score = f'<span>Вы набрали {score} баллов</span>'
            return render(request, 'game/win-lose/win.html', {'score': score})


@login_required(login_url='login')
def clarify_question(request):
    if request.POST:
        post = request.POST
        message = f'Пользователь: {post["user"]} \nID вопроса: {post["questID"]}\nВопрос: {post["question"]}'\
                  '\nСообщение: {post["message"]}'

        sendmail('Уточнение по вопросу', message, settings.EMAIL_ADMIN_USERS)
        return redirect('account')
