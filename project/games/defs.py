import random

difficulty_list = (10, 20, 30, 40, 50)


def get_template_questions(level):
    templates = {
        'J': (10, 10, 10, 10, 20, 20, 20, 20, 30, 30, 30, 30),
        'L': (10, 10, 10, 20, 20, 20, 30, 30, 30, 40, 40, 50),
        'Z': (10, 10, 20, 20, 20, 30, 30, 30, 40, 40, 50, 50),
        'M': (20, 20, 20, 30, 30, 30, 30, 40, 40, 40, 50, 50),
        'P': (30, 30, 30, 30, 40, 40, 40, 40, 50, 50, 50, 50)
    }

    level = level[0]
    return templates.get(level)


def counter(template, diff):
    return template.count(diff)


def get_question_list_separated_by_difficulty(question_instance):
    separated_question_list = []
    conditions = {'moderate': False, 'public': True}  # условия для выборки отработанных вопросов
    for difficulty in difficulty_list:
        separated_question_list.append(question_instance.objects.filter(difficulty=difficulty, **conditions))
    return separated_question_list


def q_questions(template_questions, question_instance):
    template = {'10': counter(template_questions, 10),
                '20': counter(template_questions, 20),
                '30': counter(template_questions, 30),
                '40': counter(template_questions, 40),
                '50': counter(template_questions, 50)}
    questions_separated_by_difficult = get_question_list_separated_by_difficulty(question_instance)
    for index in range(0, 5):
        difficulty = difficulty_list[index]
        question_list = list(questions_separated_by_difficult[index])
        quantity = template[str(difficulty)]
        if len(question_list) < quantity:
            return {'status': 'error', 'error': 'Not enough questions'}
        template[str(difficulty)] = random.sample(question_list, quantity)

    return template
