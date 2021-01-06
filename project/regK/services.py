from uuid import uuid4

from django.conf import settings

from main.sendmail import sendmail
from userK.models import User, ConfirmKey


def do_register(username, birthday, email, password):
    user = User.objects.create_user(username=username, birthday=birthday, email=email, password=password)
    activation_code = str(uuid4())
    ConfirmKey.objects.create(user=user, type=ConfirmKey.TypeChoices.ACCOUNT_CONFIRMATION, code=activation_code)

    confirm_url = 'https://' + settings.DOMAIN + r'/accountconfirmation/account/email?c=' + activation_code
    message_text = f'Ваша ссылка для активации аккаунта: \n {confirm_url}'
    sendmail('Активация аккаунта', message_text, email)
