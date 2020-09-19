from django.shortcuts import render, redirect
from questions.models import Questions, Category, Theme
from userK import services as user_services, models as user_models
from . import defs
from main.sendmail import sendmail
from django.conf import settings
from django.http import JsonResponse


def apiGame(request):
    p = 1
    quest_list = []

    def quest_l(questions, index):
        if questions[index]:
            for i in questions[index]:
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
            league = user_services.get_user_rating_lvl_dif(int(request.user.opLVL))['level']
        else:
            league = 'Z'
        quest_template = defs.q_template(league)
        questions = defs.q_questions(league, Questions, p)
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
    return render(request, 'game/train.html', {'title': 'ТРЕНИРОВКА ЭРУДИТ-ЛОТО'})


def win_lose(request):
    if request.GET.__contains__('status'):
        status = request.GET['status']
        score = request.GET["score"]
        if status == 'lose':
            author = f'{request.GET["author"]}'
            question = f'{request.GET["question"]}'
            correctAnswer = f'{request.GET["correctAnswer"]}'
            score = f'<span>{score} баллов</span>'
            newGame = f'{request.GET["newGame"]}'
            questID = f'{request.GET["questID"]}'
            return render(request, 'game/win-lose/wrong.html', {'question': question, 'correctAnswer': correctAnswer,
                                                                'score': score, 'author': author, 'newGame': newGame,
                                                                'questID': questID})
        elif status == 'win':
            score = f'<span>Вы набрали {score} баллов</span>'
            return render(request, 'game/win-lose/win.html', {'score': score})


def clarify_question(request):
    if request.POST:
        post = request.POST
        message = f'Пользователь: {post["user"]} \nID вопроса: {post["questID"]}\nВопрос: {post["question"]}\nСообщение: {post["message"]}'

        sendmail('Уточнение по вопросу', message, settings.EMAIL_ADMIN_USERS)
        return redirect('account')
