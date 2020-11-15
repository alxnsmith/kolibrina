from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from . import services


class MarathonWeek(View):
    def get(self, request):
        self.user = self.request.user
        marathons = services.get_list_official_marathons()
        if marathons['status'] == 'OK':
            marathon = marathons['marathons_list'][0]
        else:
            return render(self.request, 'marathon/marathon.html')
        self.marafon = services.MarathonWeek(marathon, self.user)
        get = self.request.GET
        query = list(get.keys())
        if 'pay' in query:
            response = self.pay()
            return JsonResponse(response)

        return render(self.request, 'marathon/marathon.html', {
            'user_info': services.get_user_info(self.user)
        })

    def pay(self):
        self.IS_BENEFIT_RECIPIENT = None
        if self._is_time_to_start:
            return {'status': 'error', 'error': 'Регистрация на марафон окончена, вы можете посмотреть за ходом игры.'}
        user = self.request.user
        if not self.IS_BENEFIT_RECIPIENT and user.balance >= self.marafon.instance.price:
            user.balance -= self.marafon.instance.price
            user.save()
        else:
            return {'status': 'error',
                    'error': 'Недостаточно средств, для участия - пополните баланс в личном кабинете.'}
        self.marafon.instance.players.add(user)
        return {'status': 'OK'}

    @property
    def _is_time_to_start(self):
        return timezone.now() > self.marafon.instance.date_time_start
