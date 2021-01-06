import datetime
from uuid import uuid4

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

# from games.services import get_all_nearest_events           | on 161s. It's need for avoid circular import
from main.sendmail import sendmail, sendmail_admins
from media import services as media_services
from userK.models import User, ConfirmKey
from . import forms


def do_register(username, birthday, email, password):
    user = User.objects.create_user(username=username, birthday=birthday, email=email, password=password)
    activation_code = str(uuid4())
    ConfirmKey.objects.create(user=user, type=ConfirmKey.TypeChoices.ACCOUNT_CONFIRMATION, code=activation_code)

    confirm_url = f'https://{settings.DOMAIN}{reverse("confirm_account")}?c={activation_code}'
    message_text = f'Ваша ссылка для активации аккаунта: \n {confirm_url}'
    sendmail('Активация аккаунта', message_text, email)


def activate_user(code_activation):
    key_object = ConfirmKey.objects.get(code=code_activation)
    if key_object.type != key_object.TypeChoices.ACCOUNT_CONFIRMATION:
        raise Exception('The wrong type of key!')
    user = key_object.user
    user.is_active = True
    user.save()
    key_object.delete()

    message = 'Новый пользователь прошел активацию!\n' \
              f'id: {user.id}\n' \
              f'username: {user.username}\n' \
              f'email: {user.email}'
    sendmail_admins('Новая регистрация', message)


def write_user_model(username, values):
    user_model = User.objects.get(username=username)
    fields = ['firstName', 'lastName', 'hide_my_name', 'birthday', 'gender',
              'country', 'area', 'city', 'phoneNumber', 'swPlace', 'league']

    for key in fields:
        if value := values.get(key, False):
            if key == 'firstName':
                user_model.firstName = value
            elif key == 'lastName':
                user_model.lastName = value
            elif key == 'birthday':
                user_model.birthday = value
            elif key == 'gender':
                user_model.gender = value
            elif key == 'country':
                user_model.country = value
            elif key == 'area':
                user_model.area = value
            elif key == 'city':
                user_model.city = value
            elif key == 'phoneNumber':
                user_model.phoneNumber = value
            elif key == 'swPlace':
                user_model.swPlace = value
            elif key == 'league':
                user_model.league = value

    user_model.hide_my_name = True if 'hide_my_name' in values else False

    user_model.save()
    return {'status': 'OK'}


def create_render_data(request, ):
    user_model = request.user
    max_date_field = '-'.join((str(datetime.date.today().year), datetime.date.today().strftime('%m-%d')))
    min_date_field = '-'.join((str(datetime.date.today().year - 100), datetime.date.today().strftime('%m-%d')))
    team_players_list = _get_teammates(request.user)

    data = {
        'user_info': {
            'formatted_id': f'{request.user.id}'.rjust(7, '0'),
            'level': get_user_rating_lvl_dif(user_model.rating),
            'avatar_image': request.user.avatar.url if request.user.avatar else False,
            'form': {
                'form_object': _get_form_values(user_model=user_model),
                'league': str(request.user.league),
                'maxDateField': max_date_field,
                'minDateField': min_date_field,
                'error_phone': '',
            },
        },
        'team': {
            'users_list': _get_users_and_id_list(request.user),
            'team_players_list': team_players_list,
            'new_teammate_num': len(team_players_list) + 1,
            'team_number': settings.TEAM_NUMBERS,
            'invite_teams_list': _get_invite_teams_list(request.user),
        },
        'open_for_registration': get_open_for_registration(request.user),
        'main_banner': media_services.get_banner(),
        'errors': [],
    }
    return data


def get_user_rating_lvl_dif(rating):
    def r(rating, max, deltamax, level):
        for i in range(0, 981):
            if rating < max:
                return {'rating': str(rating) + '/' + str(max), 'numLevel': i, 'level': level}
            else:
                max += deltamax

    if rating < 1000:
        max = 100
        deltamax = 100
        level = 'J (юниор)'
        return r(rating, max, deltamax, level)
    elif rating < 3000:
        max = 1000
        deltamax = 200
        level = 'L (любитель)'
        return r(rating, max, deltamax, level)
    elif rating < 6000:
        max = 3000
        deltamax = 300
        level = 'Z (знаток)'
        return r(rating, max, deltamax, level)
    elif rating < 10000:
        max = 6000
        deltamax = 400
        level = 'M (мастер)'
        return r(rating, max, deltamax, level)
    else:
        max = 10000
        deltamax = 500
        level = 'P (профи)'
        return r(rating, max, deltamax, level)


def _get_users_and_id_list(current_user):
    users_list = User.objects.filter(is_active=1)
    users_and_id_list = []
    for user in users_list:
        if user.username != current_user.username:
            user_id = str(user.id).rjust(7, '0')
            user_username = user.username
            users_and_id_list.append(f'{user_username} | {user_id}')
    return users_and_id_list


def _get_form_values(user_model):
    try:
        form = forms.EditUser(initial={
            'birthday': format(user_model.birthday, '%Y-%m-%d'),
            'gender': user_model.gender,
            'country': user_model.country,
            'area': user_model.area,
            'city': user_model.city,
            'league': user_model.league
        })
    except TypeError:
        form = forms.EditUser(initial={
            'birthday': '',
            'gender': user_model.gender,
            'country': user_model.country,
            'area': user_model.area,
            'city': user_model.city,
            'league': user_model.league
        })
    return form


def _get_name_or_blank(user):
    if user.team_set.exists():
        return user.team_set.first()
    else:
        return ''


def _get_invite_teams_list(user):
    invite_list = user.invites_set.all()
    return invite_list


def _get_teammates(user):
    if user.team_set.exists():
        return user.team_set.first().players.all()
    else:
        return ''


def get_open_for_registration(user):
    from games.services import get_all_nearest_events
    events = []
    nearest_events = get_all_nearest_events()

    for event in nearest_events['marathon_rounds']:
        events.append(EventsTableData.marathon_rounds(event, user))

    for event in nearest_events['continuous_marathons']:
        events.append(EventsTableData.continuous_marathon(event, user))

    return sorted(events, key=lambda x: x['date_time_start'])


class EventsTableData:
    @staticmethod
    def marathon_rounds(event, user):
        date_time_start = timezone.localtime(event.date_time_start)
        marathon = event.marathonweekofficial_set.first()
        num_of_rounds = marathon.rounds.count()
        code_name = 'OMWEL_round'
        pk = event.pk
        price = EventsTableData._get_price(event.price, user.discount)
        rounds = marathon.rounds.order_by('date_time_start')
        is_player = user in event.players.all()
        if num_of_rounds > 1:
            for i, round in enumerate(rounds):
                if event.pk == round.pk:
                    num_of_round = i + 1
                    num_of_rounds = f'{num_of_rounds}/{num_of_round}'

        return EventsTableData._get_row_data(
            date_time_start, marathon.code_name, marathon.id,
            num_of_rounds, price, marathon.name, code_name, pk, is_player)

    @staticmethod
    def continuous_marathon(event, user):
        date_time_start = timezone.localtime(event.date_time_start)
        num_of_rounds = event.rounds.count()
        price = EventsTableData._get_price(event.price, user.discount)
        codename = 'OMWEL_continuous'
        pk = event.pk
        is_player = user in event.players.all()

        return EventsTableData._get_row_data(
            date_time_start, event.code_name, event.id, num_of_rounds, price, event.name, codename, pk, is_player)

    @staticmethod
    def _get_row_data(date_time_start, code_name_view, id, number_of_rounds, price, name, codename, pk, is_player):
        return {
            'date_time_start': date_time_start,
            'date_start': format(date_time_start, '%d.%m.%y'),
            'time_start': format(date_time_start, '%H:%M'),
            'code_name_view': code_name_view,
            'id': id,
            'number_of_rounds': number_of_rounds,
            'price': price,
            'name': name or '______________________',
            'code_name': codename,
            'pk': pk,
            'is_player': is_player
        }

    @staticmethod
    def _get_price(price, discount):
        raw_price = price - (price / 100 * discount)
        price = ','.join((str(int(raw_price)), str(raw_price).split('.')[-1].rjust(2, '0')))
        return price
