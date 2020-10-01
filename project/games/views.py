from django.shortcuts import render, redirect, Http404
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from questions.models import Question
from userK import services as user_services, models as user_models
from . import defs, services
from main.sendmail import sendmail
from django.conf import settings
from django.http import JsonResponse


def api_train(request):
    quest_list = []

    def quest_l(questions_list, index):
        if questions_list[index]:
            for i in questions_list[index]:
                d = model_to_dict(i)
                city = i.author.city
                print('{0} {1}, г.{2}'.format(
                        i.author.firstName,
                        i.author.lastName, city,
                    ))
                if user_models.CustomUser.objects.get(id=d['author']).hideMyName or not city:
                    d['author'] = str(i.author)
                else:
                    d['author'] = '{0} {1}, г.{2}'.format(
                        i.author.firstName,
                        i.author.lastName, city,
                    )
                d['category'] = str(i.category)
                d['theme'] = str(i.theme)
                del d['purpose'], d['premoderate'],
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


def win_lose(request):
    get = request.GET
    if 'score' in get and 'status' in get:
        status = get['status']
        score = get["score"]
        if status == 'lose':
            author = f'{get["author"]}'
            question = f'{get["question"]}'
            correct_answer = f'{get["correctAnswer"]}'
            score = f'<span>{score} баллов</span>'
            new_game = f'{get["newGame"]}'
            quest_id = f'{get["questID"]}'
            return render(request, 'game/win-lose/wrong.html', {'question': question, 'correctAnswer': correct_answer,
                                                                'score': score, 'author': author, 'newGame': new_game,
                                                                'questID': quest_id})
        elif status == 'win':
            score = f'<span>Вы набрали {score} баллов</span>'
            return render(request, 'game/win-lose/win.html', {'score': score, 'train': get.get('train')})
        elif status == 'lose_tournament_week':
            raw_data = services.create_render_data_for_tournament_week_el(request)
            if raw_data['status'] == 'error':
                raise Http404(raw_data['error'])
            del raw_data['status']
            data = raw_data
            data['score'] = score
            data['attempt'] = True if int(get['attempt']) < 3 else False
            data['timer'] = get['time']
            data['correct_answer'] = get['correct_answer']
            data['tournament_author'] = get['author']
            data['question_text'] = get['question']
            data['answer'] = get['answer']
            return render(request, 'game/win-lose/tournament-week-wrong.html', data)
    else:
        raise Http404('')


@login_required(login_url='login')
def clarify_question(request):
    if request.POST:
        post = request.POST
        message = f'Пользователь: {post["user"]} \nID вопроса: {post["questID"]}\nВопрос: {post["question"]}'\
                  '\nСообщение: {post["message"]}'

        sendmail('Уточнение по вопросу', message, settings.EMAIL_ADMIN_USERS)
        return redirect('account')
