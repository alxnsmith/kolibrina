import uuid

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
