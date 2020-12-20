import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from yandex_checkout import Configuration

from .services import make_payment_and_get_url, UserBalance


class PaymentAPI(View):
    config = Configuration.configure(**settings.YANDEX_CHECKOUT_CONFIG)

    @staticmethod
    def get(request):
        user = request.user
        payment_method = request.GET['payment_method']
        value = request.GET['value']
        confirmation_url = make_payment_and_get_url(str(user),
                                                    str(user.id),
                                                    int(value),
                                                    str(payment_method))
        return redirect(confirmation_url)


class Notifications(View):
    @staticmethod
    def post(request):
        notification = json.loads(request.body)
        if not notification['object'].get('test') or settings.DEBUG:
            if notification['event'] == 'payment.succeeded' and notification['object']['paid']:
                user_id = notification['object']['metadata']['userID']
                amount = notification['object']['amount']
                UserBalance.deposit(amount, user_id)
        return JsonResponse({'status': 'OK'})
