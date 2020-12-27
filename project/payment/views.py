import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from yandex_checkout import Configuration

from .services import make_payment_and_get_url, UserBalance
from yandex_checkout.client import BadRequestError


class PaymentAPI(View):
    config = Configuration.configure(**settings.YANDEX_CHECKOUT_CONFIG)

    @staticmethod
    def get(request):
        user = request.user
        payment_method = request.GET['payment_method']
        value = request.GET['value']
        try:
            args = (str(user), str(user.id), int(value), str(payment_method), settings.DOMAIN)
            confirmation_url = make_payment_and_get_url(*args)
            return JsonResponse({
                'status': 'ok',
                'redirect_to': confirmation_url
            })
        except BadRequestError as exception:
            error = {'status': 'error', 'text_error': exception.args[0]}
            return JsonResponse(error)


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
