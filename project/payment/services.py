import uuid

from userK.models import User
from django.conf import settings
from yandex_checkout import Payment


def make_payment_and_get_url(user: str, user_id: str, value: int, payment_method: str):
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": f"{value}.00",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": f"{payment_method}"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"{settings.DOMAIN}"
        },
        "capture": True,
        "description": f"Пополнение баланса пользователя {user}",
        "metadata": {
            "userID": f"{user_id}"
        }
    }, idempotence_key)

    confirmation_url = payment.confirmation.confirmation_url
    return confirmation_url


class UserBalance:
    @staticmethod
    def pay(amount: dict, user_id: int):
        if amount['currency'] != 'RUB':
            return False
        user = User.objects.get(id=user_id)
        user.balance = round(float(user.balance - amount['value']), 2)
        user.save()
        return True

    @staticmethod
    def deposit(amount: dict, user_id: str):
        if amount['currency'] != 'RUB':
            return False
        user = User.objects.get(id=user_id)
        user.balance = round(float(user.balance + float(amount['value'])), 2)
        user.save()
        return True

    @staticmethod
    def check_balance(user, cost):
        return user.balance >= cost
