import re


def phone_isValid(number, User, data):
    phoneNumbers = []
    regexNum = re.match(r'\+\d (\d{3}) (\d{3})-(\d{2})-(\d{2})', number)
    for user in User.objects.all():
        phoneNumbers.append(user.phoneNumber)
    if not phoneNumbers.__contains__(number) and regexNum.__str__() == 'None':
        data['errors'].append('Введите номер телефона')
        data['error_phone'] = 'border-red'
    elif re.match(r'8\d{10}', number):
        return number, data['errors'], data['error_phone']
    elif phoneNumbers.__contains__('8' + ''.join(regexNum.group(1, 2, 3, 4))):
        data['errors'].append('Этот номер телефона уже используется в другом аккаунте')
        data['error_phone'] = 'border-red'
    else:
        donePhone = regexNum.group(1, 2, 3, 4)
        return donePhone, data['errors'], data['error_phone']
    return '', data['errors'], data['error_phone']
