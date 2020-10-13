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
                        question, correct_answer, answer2, answer3, answer4, pos):
    return models.Question.objects.create(author_id=author_id,
                                          category_id=category_id,
                                          theme_id=theme_id,
                                          difficulty=difficulty,
                                          question=question.strip(),
                                          correct_answer=correct_answer.strip(),
                                          answer2=answer2.strip(),
                                          answer3=answer3.strip(),
                                          answer4=answer4.strip(),
                                          pos=pos, )


def get_questions_from_tournament(tournament):
    return tournament.questions.all()


def add_marafon_theme_block(author: object, questions: list):
    themes_check = set()
    for i in questions:
        themes_check.add(i.theme_id)
    if len(themes_check) == 1:
        theme_id = questions[0].theme_id
    else:
        return False

    block = models.MarafonThemeBlock.objects.create(author=author, theme_id=theme_id)

    for i in questions:
        block.questions.add(i)
    return block


def add_marafon(post, author: object):
    question_list = post['question_list']
    question_blocks = {1: [], 2: [], 3: [], 4: []}
    for i in question_list:
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
        question_blocks[i] = add_marafon_theme_block(author, question_blocks[i])
    marafon_instance = models.Marafon.objects.create(purpose=post['purpose'], author=author)
    for i in question_blocks:
        marafon_instance.question_blocks.add(question_blocks[i].id)
    return {'status': 'OK'}
