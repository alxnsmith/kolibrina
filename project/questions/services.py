from django.utils import timezone

from questions.models import Marafon, Tournament
from . import models


def add_theme_to_category(post):
    cat = post['cat']
    theme = post['theme']
    models.Theme.objects.create(category_id=cat, theme=theme)
    return {'status': 'OK'}


def add_tournament_week(post):
    question_list = post['tournament']
    if len(question_list) != 35:
        return {'status': 'error', 'error': 'Not full tournament'}
    author_id = post['tournament']['01']['author_id']
    tournament = _create_tournament(author_id, models.Tournament.Purposes.TOURNAMENT_WEEK_ER_LOTTO)
    question_list_models = []
    for q in question_list:
        pos = question_list[q]['pos']
        if pos.startswith('0'):
            question_list[q]['pos'] = pos[1:]
        elif pos.startswith('д'):
            question_list[q]['pos'] = f'd{pos[1:]}'
        elif pos.startswith('замена'):
            question_list[q]['pos'] = 'zamena'
        q['purpose'] = 'TournamentWeek'
        question_list_models.append(_add_question_to_db(**question_list[q]))
    for i in question_list_models:
        tournament.questions.add(i)
    return {'status': 'OK'}


def add_question(request):
    items = request.POST.dict()
    items['author_id'] = request.user.id
    if 'csrfmiddlewaretoken' in items:
        del items['csrfmiddlewaretoken']
    models.Question.objects.create(**items)


def _create_tournament(author_id, purpose):
    return models.Tournament.objects.create(author_id=author_id, purpose=purpose)


def _add_question_to_db(author_id, category_id, theme_id, difficulty,
                        question, correct_answer, answer2, answer3, answer4, pos, purpose=None, is_active=False):
    purposes = {
        'Training': 1,
        'Marafon': 2,
        'TournamentWeek': 3
    }

    return models.Question.objects.create(author_id=author_id,
                                          category_id=category_id,
                                          theme_id=theme_id,
                                          difficulty=difficulty,
                                          question=question.strip(),
                                          correct_answer=correct_answer.strip(),
                                          answer2=answer2.strip(),
                                          answer3=answer3.strip(),
                                          answer4=answer4.strip(),
                                          pos=pos,
                                          purpose_id=purposes.get(purpose))


def get_questions_from_tournament(tournament):
    return tournament.questions.all()


def add_marafon_theme_block(author: object, questions: list, is_active=False):
    themes_check = set()
    for i in questions:
        themes_check.add(i.theme_id)
    if len(themes_check) == 1:
        theme_id = questions[0].theme_id
    else:
        return False

    block = models.MarafonThemeBlock.objects.create(author=author, theme_id=theme_id, is_active=is_active)

    for i in questions:
        block.questions.add(i)
    return block


def add_marafon(post, author: models.User):
    question_list = post['question_list']
    question_blocks = {1: [], 2: [], 3: [], 4: []}

    for i in question_list:
        question_list[i]['pos'] = int(question_list[i]['pos'])
        question_list[i]['purpose'] = 'Marafon'
        question_model = _add_question_to_db(**question_list[i])
        if str(i).startswith('1'):
            question_blocks[1].append(question_model)
        if str(i).startswith('2'):
            question_blocks[2].append(question_model)
        if str(i).startswith('3'):
            question_blocks[3].append(question_model)
        if str(i).startswith('4'):
            question_blocks[4].append(question_model)
    is_active = True if author.is_staff else False
    for i in question_blocks:
        question_blocks[i] = add_marafon_theme_block(author, question_blocks[i], is_active)
    marafon_instance = models.Marafon.objects.create(purpose=post['purpose'], author=author)
    for i in question_blocks:
        marafon_instance.question_blocks.add(question_blocks[i].id)
    return {'status': 'OK'}


def get_tournament_instance(tournament_shortname):
    date_range = (timezone.now() - timezone.timedelta(days=7), timezone.now())  # last 7 days
    active_tournaments_list = Tournament.objects.filter(
        is_active=True, purpose=tournament_shortname,
        date__range=date_range)
    if active_tournaments_list.exists():
        tournament_model = active_tournaments_list.order_by('date')[0]
    else:
        tournament_model = {'status': 'error', 'error': 'Empty'}
    return tournament_model


def get_marafon_instance():
    active_marafon_list = Marafon.objects.filter(
        is_active=True, purpose='MWEL', official=True, price__isnull=False, date_time_start__isnull=False
    )
    if active_marafon_list.exists():
        marafon = active_marafon_list.order_by('date_time_start')[0]
    else:
        marafon = {'status': 'error', 'error': 'Empty'}
    return marafon


def get_open_for_registration():
    reg_list = [get_marafon_instance(), ]
    return reg_list
