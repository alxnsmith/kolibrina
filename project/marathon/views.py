from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from . import services
from games.services import get_user_info


class MarathonWeek(View):
    def get(self, request):
        self.user = self.request.user
        if round_instance := services.get_nearest_official_marathon_round():
            self.round = services.MarathonWeekGP(round_instance['instance'], round_instance['date_time_start'])
            get = self.request.GET
            query = list(get.keys())
            if 'pay' in query:
                response = self.pay()
                return JsonResponse(response)

        return render(self.request, 'marathon/marathon.html', {
            'user_info': get_user_info(self.user),
            'game_type': 'marathon_week_official',
        })

    def pay(self):
        if self._is_time_to_start:
            return {'status': 'error', 'error': 'Регистрация на марафон окончена, вы можете посмотреть за ходом игры.'}
        user = self.request.user
        if user.balance >= self.round.instance.price:
            user.balance -= self.round.instance.price
            user.save()
        else:
            return {'status': 'error',
                    'error': 'Недостаточно средств, для участия - пополните баланс в личном кабинете.'}
        self.round.instance.players.add(user)
        return {'status': 'OK'}

    @property
    def _is_time_to_start(self):
        return timezone.now() > self.round.instance.date_time_start
