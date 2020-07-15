import random


def q_template(u):
    if u == 'J':
        return 10, 10, 10, 10, 20, 20, 20, 20, 30, 30, 30, 30,
    if u == 'L':
        return 10, 10, 10, 20, 20, 20, 30, 30, 30, 40, 40, 50,
    if u == 'Z':
        return 10, 10, 20, 20, 20, 30, 30, 30, 40, 40, 50, 50,
    if u == 'M':
        return 20, 20, 20, 30, 30, 30, 30, 40, 40, 40, 50, 50,
    if u == 'P':
        return 30, 30, 30, 30, 40, 40, 40, 40, 50, 50, 50, 50,


def counter(template, diff):
    return template.count(diff)


def dif_q(q):
    dif = []
    for i in 10, 20, 30, 40, 50:
        dif.append(q.objects.filter(difficulty=i))
    return dif


def q_questions(league, q):
    t = q_template(league)
    template = {'10': counter(t, 10), '20': counter(t, 20), '30': counter(t, 30),
                '40': counter(t, 40), '50': counter(t, 50)}
    q1 = dif_q(q)
    d = 10
    for s in range(0, 5):
        a = []
        for i in q1[s]:
            if not i.premoderate:
                a.append(i)
        template[str(d)] = random.sample(a, template[str(d)])
        d += 10
    return template
