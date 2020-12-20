def check_fill_profile(request):
    if not request.user.firstName and not request.user.lastName and not request.user.city:
        errors = [{'link': '/account', 'tlink': 'Заполните ',
                   'error': 'свой профиль для полноценного пользования сервисом.',
                   }]
        return errors

