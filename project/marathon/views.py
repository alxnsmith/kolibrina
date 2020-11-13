from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from . import services


class MarathonWeek(View):
    IS_BENEFIT_RECIPIENT = None

    def __init__(self):
        super(MarathonWeek, self).__init__()

    def get(self, request):
        self.marafon = services.MarafonWeek(self.request.user)
        self.user = self.request.user
        get = self.request.GET
        query = list(get.keys())
        if 'info' in query:
            response = self.marafon.info
            return JsonResponse(response)
        elif 'pay' in query:
            response = self.pay()
            return JsonResponse(response)

        info = self.marafon.info
        if info['status'] == 'OK':
            return render(self.request, 'game/marafon.html', {
                'marafon_info': info,
                'user_info': services.get_user_info(self.user)
            })
        else:
            return redirect('account')

    def pay(self):
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
