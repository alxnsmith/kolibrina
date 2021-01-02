from django.utils import timezone

from games.models import Tournament
from marathon.models import MarathonRound
from .models import Theme, Question, MarathonThemeBlock, User


class Purpose:
    Training = 1
    MarathonWeek = 2
    OfficialMarathonWeek = 3
    TournamentWeek = 4


def add_theme_to_category(post):
    cat = post['cat']
    theme = post['theme']
    Theme.objects.create(category_id=cat, theme=theme)
    return {'status': 'OK'}


def add_tournament_week(post, author: User):
    question_list = post['tournament']
    if len(question_list) != 35:
        return {'status': 'error', 'error': 'Not full tournament'}
    tournament = Tournament.objects.create(author=author, purpose_id=Purpose.TournamentWeek)
    moderate = False if User.is_staff else True
    for pos, question in question_list.items():
        if pos.startswith('0'):
            question['pos'] = pos[1:]
        elif pos.startswith('д'):
            question['pos'] = pos.replace('д', 'd')
        elif pos.startswith('замена'):
            question['pos'] = 'zamena'
        question['purpose_id'] = Purpose.TournamentWeek
        question['moderate'] = moderate
        tournament.questions.add(
            _add_question_to_db(**question)  # returns question model and add to tournament
        )
    return {'status': 'OK'}


def add_question(request):
    items = request.POST.dict()

    items['author_id'] = request.user.id
    items.pop('csrfmiddlewaretoken')
    items.pop('category_id')

    Question.objects.create(**items)


def _add_question_to_db(author_id, category_id, theme_id, difficulty,
                        question, correct_answer, answer2, answer3, answer4, pos, purpose_id=None, moderate=True):

    return Question.objects.create(
        author_id=author_id,
        theme_id=theme_id,
        difficulty=difficulty,
        question=question.strip(),
        correct_answer=correct_answer.strip(),
        answer2=answer2.strip(),
        answer3=answer3.strip(),
        answer4=answer4.strip(),
        pos=pos,
        purpose_id=purpose_id,
        moderate=moderate
    )


def get_questions_from_tournament(tournament):
    return tournament.questions.all()


def add_marafon_theme_block(author: User, questions: list):
    themes_check = set()
    is_active = True if author.is_staff else False
    for i in questions:
        themes_check.add(i.theme_id)
    if len(themes_check) == 1:
        theme_id = questions[0].theme_id
    else:
        return False

    block = MarathonThemeBlock.objects.create(author=author, theme_id=theme_id, is_active=is_active)

    for i in questions:
        block.questions.add(i)
    return block


def add_theme_blocks(post, author: User):
    question_list = post['question_list']
    question_blocks = {1: [], 2: [], 3: [], 4: []}
    block_list = []

    for i in question_list:
        question_list[i]['pos'] = int(question_list[i]['pos'])
        question_list[i]['purpose_id'] = Purpose.MarathonWeek
        question_model = _add_question_to_db(**question_list[i])
        if str(i).startswith('1'):
            question_blocks[1].append(question_model)
        if str(i).startswith('2'):
            question_blocks[2].append(question_model)
        if str(i).startswith('3'):
            question_blocks[3].append(question_model)
        if str(i).startswith('4'):
            question_blocks[4].append(question_model)
    for i in question_blocks:
        block = add_marafon_theme_block(author, question_blocks[i])
        block_list.append(block)
    if author.is_staff:
        marathon = MarathonRound.objects.create(author=author)
        for block in block_list:
            marathon.question_blocks.add(block)
    return {'status': 'OK'}


def get_tournament_instance(tournament_shortname):
    tournament_model = None
    date_range = (timezone.now() - timezone.timedelta(days=7), timezone.now())  # last 7 days
    active_tournaments_list = Tournament.objects.filter(
        is_active=True, purpose__codename=tournament_shortname,
        date__range=date_range
    )
    if active_tournaments_list.exists():
        tournament_model = active_tournaments_list.order_by('date').first()
    return tournament_model


