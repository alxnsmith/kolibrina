import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect, Http404
from django.template import loader
from django.utils import timezone
from django.views import View

from main.sendmail import sendmail
from questions.models import Question
from userK import services as user_services, models as user_models
from . import defs, services


def api_train(request):
    quest_list = []

    def quest_l(questions_list: dict, key: str):
        if questions_list[key]:
            for i in questions_list[key]:
                d = model_to_dict(i)
                city = i.author.city
                if user_models.User.objects.get(id=d['author']).hideMyName or not city:
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
            league = user_services.get_user_rating_lvl_dif(float(request.user.rating))['level']
        else:
            league = 'Z'
        quest_template = defs.get_template_questions(league)
        questions = defs.q_questions(league, Question)
        if 'error' in questions:
            return JsonResponse(questions)
        questions = {'q10': questions['10'],
                     'q20': questions['20'],
                     'q30': questions['30'],
                     'q40': questions['40'],
                     'q50': questions['50']}
        quest_l(questions, 'q10')
        quest_l(questions, 'q20')
        quest_l(questions, 'q30')
        quest_l(questions, 'q40')
        quest_l(questions, 'q50')

        response = {'quest_list': quest_list, 'league': league, 'quest_template': quest_template}
        return JsonResponse(response, safe=False)


@login_required()
def tournaments(request):
    return render(request, 'game/tournaments.html')


def train(request):
    raw_data = services.create_render_data_for_train_el()
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
        message = f'Пользователь: {post["user"]} \nID вопроса: {post["questID"]}\nВопрос: {post["question"]}' \
                  f'\nСообщение: {post["message"]}'

        sendmail('Уточнение по вопросу', message, settings.EMAIL_ADMIN_USERS)
        return redirect('account')


class MarafonWeek(View):
    BENEFIT_RECIPIENT = None

    def __init__(self):
        super(MarafonWeek, self).__init__()
        self.queries = {
            'info': self.get_marafon_info,
            'pay': self.pay,
        }
        self.marafon = services.get_marafon_instance()

    def get(self, request):
        self.user = self.request.user
        get = self.request.GET
        self.BENEFIT_RECIPIENT = Group.objects.get(name='Benefit recipients') in self.request.user.groups.all()
        query = list(get.keys())
        if len(query) == 1:
            if query[0] in list(self.queries.keys()):
                return JsonResponse(self.queries[query[0]]())

        info = self.get_marafon_info()
        if info['status'] == 'OK':
            return render(self.request, 'game/marafon.html', {
                'marafon_info': info,
                'user_info': self.get_user_info()
            })
        else:
            return redirect('account')

    def get_user_info(self):
        last_month_date_range = (timezone.now() - datetime.timedelta(days=30), timezone.now())
        return {'first_name': self.user.firstName,
                'last_name': self.user.lastName,
                'city': self.user.city,
                'league': self.user.get_league_display(),
                'level': services.user_services.get_user_rating_lvl_dif(self.user.rating),
                'month_score': services.get_sum_score_user(self.user, last_month_date_range),
                'total_score': services.get_sum_score_user(self.user),
                'avatar': services.user_services.media_services.get_avatar(self.user),
                }

    def get_marafon_info(self):
        if type(self.marafon) is dict and self.marafon['status'] == 'error':
            return self.marafon
        users = self.marafon.players.all()
        return {
            'status': 'OK',
            'id': self.marafon.id,
            'name': self.marafon.name,
            'author': self.marafon.author.username,
            'author_firstname': self.marafon.author.firstName,
            'author_lastname': self.marafon.author.lastName,
            'author_city': self.marafon.author.city,
            'players': [user.username for user in users],
            'response_timer': self.marafon.response_timer,
            'choose_timer': self.marafon.choose_timer,
            'price': '0' if self.BENEFIT_RECIPIENT else self.marafon.price,
            'date_start': str(self.marafon.date_time_start.timestamp()),
            'access': self.request.user in users,
            'time_to_start': self._time_to_start,
            'number_of_theme_blocks': list(range(0, len(self.marafon.question_blocks.all())))
        }

    def pay(self):
        self.marafon = services.get_marafon_instance()
        if self._time_to_start:
            return {'status': 'error', 'error': 'Регистрация на марафон окончена, вы можете посмотреть за ходом игры.'}
        user = self.request.user
        if not self.BENEFIT_RECIPIENT and user.balance >= self.marafon.price:
            user.balance -= self.marafon.price
            user.save()
        else:
            return {'status': 'error',
                    'error': 'Недостаточно средств, для участия - пополните баланс в личном кабинете.'}
        self.marafon.players.add(user)
        return {'status': 'OK'}

    @property
    def _time_to_start(self):
        return timezone.now() > self.marafon.date_time_start
