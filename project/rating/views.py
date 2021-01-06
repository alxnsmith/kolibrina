from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from . import services
from games.services import get_user_info
from account.models import User as User
from account.services import get_user_rating_lvl_dif
from marathon.models import MarathonWeekOfficial


def ratings(request):
    opLVL_users = User.objects.extra(select={'rating': 'CAST(rating AS INTEGER)'}).order_by('-rating')

    league_count = {'l1': User.objects.filter(league='l1').__len__(),
                    'l2': User.objects.filter(league='l2').__len__(),
                    'l3': User.objects.filter(league='l3').__len__(),
                    'l4': User.objects.filter(league='l4').__len__(),
                    'l5': User.objects.filter(league='l5').__len__(),
                    'l6': User.objects.filter(league='l6').__len__()}

    level = {'J': 0, 'L': 0, 'Z': 0, 'M': 0, 'P': 0}

    for i in opLVL_users:
        if int(i.rating) < 1000:
            level['J'] += 1
        elif int(i.rating) < 3000:
            level['L'] += 1
        elif int(i.rating) < 6000:
            level['Z'] += 1
        elif int(i.rating) < 10000:
            level['M'] += 1
        else:
            level['P'] += 1

    opLVL_top15 = []

    for i in opLVL_users[:15]:
        opLVL_top15.append({'hide_my_name': i.hide_my_name,
                            'lvl': '{0} / {1}'.format(get_user_rating_lvl_dif(i.rating)['level'],
                                                      get_user_rating_lvl_dif(i.rating)['numLevel']),
                            'opLVL': i.rating,
                            'firstName': i.firstName,
                            'lastName': i.lastName,
                            'city': i.city,
                            'username': i.username})

    return render(request, 'rating/ratings.html', {'league_count': league_count, 'level': level,
                                                   'opLVL_top15': opLVL_top15})


class SummaryMarathonWeek(View):
    def get(self, request, id):
        get = request.GET
        if get:
            if 'get_data' in get:
                data = services.get_data(id)
                return JsonResponse(data)

        self.user = self.request.user
        get_object_or_404(MarathonWeekOfficial, id=int(id))
        return render(request, 'rating/summary-of-round.html', {
            'user_info': get_user_info(self.user),
        })
