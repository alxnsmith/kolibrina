from . import models


def add_theme_to_category(post):
    cat = post['cat']
    theme = post['theme']
    models.Theme.objects.create(category_id=cat, theme=theme)
    return {'status': 'OK'}


def add_tournament(post):
    question_list = post['tournament']
    if len(question_list) != 35:
        return {'status': 'error', 'error': 'Not full tournament'}
    author_id = post['tournament']['01']['author_id']
    author = models.CustomUser.objects.get(id=author_id)
    _create_tournament(author_id)
    tournament = author.tournament_set.all().order_by('create_date').last()
    for q in question_list:
        print(question_list[q]['position'])
        pos = question_list[q]['position']
        if pos.startswith('0'):
            question_list[q]['position'] = pos[1:]
        elif pos.startswith('д'):
            question_list[q]['position'] = f'd{pos[1:]}'
        elif pos.startswith('замена'):
            question_list[q]['position'] = 'zamena'
        _add_question_to_db(**question_list[q], tournament=tournament)
    return {'status': 'OK'}


def _create_tournament(author_id):
    models.Tournament.objects.create(author_id=author_id)


def _add_question_to_db(author_id, category_id, theme_id, difficulty,
                        question, correct_answer, answer2, answer3, answer4, position, tournament):
    models.Question.objects.create(author_id=author_id,
                                   category_id=category_id,
                                   theme_id=theme_id,
                                   difficulty=difficulty,
                                   question=question,
                                   correct_answer=correct_answer,
                                   answer2=answer2,
                                   answer3=answer3,
                                   answer4=answer4,
                                   pos=position,
                                   for_tournament=tournament)
