from . import models


def add_theme_to_category(post):
    cat = post['cat']
    theme = post['theme']
    models.Theme.objects.create(category_id=cat, theme=theme)
    return {'status': 'OK'}


def add_question(post):
    models.Question.objects.create(
        author_id=int(post['author']),
        category_id=int(post['category']),
        theme_id=int(post['theme']),
        difficulty=int(post['difficulty']),
        question=post['question'],
        corectAnsw=post['corectAnsw'],
        answer2=post['answer2'],
        answer3=post['answer3'],
        answer4=post['answer4'],
    )