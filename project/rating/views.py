from django.shortcuts import render
from userK.models import CustomUser as User
from userK.level import op


def ratings(request):
    opLVL_users = User.objects.extra(
    select={'opLVL': 'CAST(opLVL AS INTEGER)'}
).order_by('-opLVL')
    league_count = {'l1': User.objects.filter(league='l1').__len__(), 'l2': User.objects.filter(league='l2').__len__(),
                    'l3': User.objects.filter(league='l3').__len__(), 'l4': User.objects.filter(league='l4').__len__(),
                    'l5': User.objects.filter(league='l5').__len__(), 'l6': User.objects.filter(league='l6').__len__()}
    level = {'J': 0, 'L': 0, 'Z': 0, 'M': 0, 'P': 0}

    for i in opLVL_users:
        if int(i.opLVL) < 1000:
            level['J'] += 1
        elif int(i.opLVL) < 3000:
            level['L'] += 1
        elif int(i.opLVL) < 6000:
            level['Z'] += 1
        elif int(i.opLVL) < 10000:
            level['M'] += 1
        else:
            level['P'] += 1

    opLVL_top15 = []

    for i in opLVL_users[:15]:
        opLVL_top15.append({'hideMyName': i.hideMyName, 'lvl': '{0}-{1}'.format(op(i.opLVL)['dif'], op(i.opLVL)['lvl']),
                            'opLVL': i.opLVL, 'firstName': i.firstName, 'lastName': i.lastName, 'city': i.city,
                            'username': i.username})

    return render(request, 'rating/ratings.html', {'league_count': league_count, 'level': level,
                                                   'opLVL_top15': opLVL_top15})
