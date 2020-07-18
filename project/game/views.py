from django.shortcuts import render, HttpResponse
from addquestion.models import Questions, Category, Theme
from userK import level, models
from . import defs


def tournaments(request):
    return render(request, 'game/tournaments.html')


def train(request):
    def quest_l(questions, index):
        if questions[index]:
            for i in questions[index]:
                d = i.__dict__
                city = models.CustomUser.objects.get(id=d['author_id']).city
                if models.CustomUser.objects.get(id=d['author_id']).hideMyName or not city:
                    d['author'] = models.CustomUser.objects.get(id=d['author_id']).username
                else:
                    d['author'] = '{0} {1}, г.{2}'.format(
                        models.CustomUser.objects.get(id=d['author_id']).firstName,
                        models.CustomUser.objects.get(id=d['author_id']).lastName, city,
                    )
                d['category'] = str(Category.objects.get(id=d['category_id']))
                d['theme'] = str(Theme.objects.get(id=d['theme_id']))
                del d['_state'], d['id'], d['premoderate'], d['author_id'], d['category_id'], d['theme_id'],
                quest_list.append(d)

    league = level.op(int(request.user.opLVL))['league']
    print(league)
    # u = defs.q_questions(defs.q_template(u), Questions.objects.all())
    questions = defs.q_questions(league, Questions)
    questions = {'q10': questions['10'], 'q20': questions['20'], 'q30': questions['30'],
                 'q40': questions['40'], 'q50': questions['50']}
    quest_list = []
    quest_l(questions, 'q10')
    quest_l(questions, 'q20')
    quest_l(questions, 'q30')
    quest_l(questions, 'q40')
    quest_l(questions, 'q50')
    return render(request, 'game/train.html', {'quest_list': quest_list, 'league': league})


def win_lose(request):
    if request.GET.__contains__('status'):
        status = request.GET['status']
        if status == 'lose':
            author = '{0}'.format(request.GET['author'])
            question = '{0}'.format(request.GET['question'])
            correctAnswer = '{0}'.format(request.GET['correctAnswer'])
            score = '<span>{0} баллов</span>'.format(request.GET['score'])
            newGame = '{0}'.format(request.GET['newGame'])
            return render(request, 'game/win-lose/wrong.html', {'question': question, 'correctAnswer': correctAnswer,
                                                                'score': score, 'author': author, 'newGame': newGame})
        elif status == 'win':
            score = '<span>Вы набрали {0} баллов</span>'.format(request.GET['score'])
            return render(request, 'game/win-lose/win.html', {'score': score})
