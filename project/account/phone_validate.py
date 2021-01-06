import re
from account.models import User as User


def phone_validate(number):
    phone_list = []
    for user in User.objects.all():
        phone_list.append(user.phoneNumber)
    regex_num = re.match(r'\+7 9(\d{2}) (\d{3})-(\d{2})-(\d{2})', number)
    if not number:
        return {'status': 'error', 'error': 'Введите номер телефона'}

    if regex_num is None:
        return {'status': 'error', 'error': 'Введите корректный номер телефона'}

    phone = '89'+''.join(regex_num.group(1, 2, 3, 4))
    if phone in phone_list:
        return {'status': 'error', 'error': 'Этот номер телефона уже используется в другом аккаунте'}
    if not re.match(r'8\d{10}', phone):
        return {'status': 'error', 'error': 'Что то произошло не так, попробуйте еще раз'}
    return {'status': 'OK', 'phone': phone}
