from django.shortcuts import render


def check_fill_profile(request, template):
    if not request.user.firstName and not request.user.lastName and not request.user.city:
        data = {'errors': [
            {'link': '/account',
             'tlink': 'Заполните ',
             'error': 'свой профиль для полноценного пользования сервисом.',
             }
        ]}
        return {'status': 'error', 'response': render(request, template, data)
                }
    else:
        return {'status': 'OK'}
