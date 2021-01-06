from django.core.exceptions import ObjectDoesNotExist

from account.models import User
from .models import Team


def set_number_on_the_team(username, number):
    user = User.objects.get(username=username)
    team_object = user.team_set.first()
    occupied_player_numbers = [i['number_in_the_team'] for i in team_object.players.values('number_in_the_team')]
    if number in occupied_player_numbers:
        return {'status': 'error', 'error': 'This number is occupied'}
    user.number_in_the_team = number
    user.save()
    return {'status': 'OK'}


def del_player_from_team(username: str, team: Team):
    player = User.objects.filter(username=username)
    if player.exists():
        player = player.first()
        check_team = player.team_set.first()
        if check_team == team:
            check_team.players.remove(player)
            _reset_number_in_the_team(player)
            _reset_team_role(player)
            return {'status': 'OK'}
        else:
            return {'status': 'error', 'error': "Player is not a member of this team"}
    else:
        return {'status': 'error', 'error': 'There is no such user!'}


def delete_team(user):
    team_role = user.team_role
    team = user.team_set.first()
    if user in team.players.all() and team_role == 'COMMANDER':
        _reset_team_role(user)
        _reset_number_in_the_team(user)
        team.delete()
        return {'status': 'OK'}


def add_player_to_invite_list(user_id: str, team: Team):
    invitee = User.objects.get(id=user_id)
    if invitee not in team.invites.all():
        team.invites.add(invitee)
        return {'status': 'OK'}
    return {'status': 'error', 'error': 'This invitation is already there'}


def get_team_info(team, user):
    try:
        team_object = Team.objects.get(name=team)
    except ObjectDoesNotExist:
        return {'Error': 'Нет такой команды'}
    players_list = list(team_object.players.values('id', 'username', 'team_role', 'number_in_the_team'))
    players = _create_dict_with_user_models(players_list)
    if not str(user) in players['list']:
        return {'Error': 'Вы не состоите в этой команде, доступ закрыт.'}
    score = team_object.score
    last_game_date = team_object.last_game_date
    data = {
        'team': team,
        'players': players_list,
        'score': score,
        'last_game_date': last_game_date,
    }
    return data


def _create_dict_with_user_models(players_list):
    players = {'list': []}
    for i, player in enumerate(players_list):
        players[i] = _User(**player)
        players['list'].append(players[i].username)
    return players


def set_player_team_role(user, put):
    role = put['role']
    teammate_list = user.team_set.first().players.all()
    if user.team_role == 'COMMANDER':
        if 'username' in put:
            if teammate_list.filter(username=put['username']).exists():
                user = teammate_list.get(username=put['username'])
    empty_places_list = _check_empty_place_in_team_roles(teammate_list=teammate_list)
    if role == 'CAPTAIN':
        if empty_places_list['COMMANDER'] == 'OK':
            _set_team_role(user, role)
        else:
            return {'status': 'error', 'error': 'Commander place is not empty!'}
    if role == 'LEGIONARY':
        if empty_places_list['LEGIONARY'] == 'OK':
            _set_team_role(user, role)
        else:
            return {'status': 'error', 'error': 'There many to Legionaries'}
    elif role == 'BASIC':
        if empty_places_list['BASIC'] == 'OK':
            _set_team_role(user, role)
        else:
            return {'status': 'error', 'error': 'There many to Basics'}

    return {'status': 'OK'}


def join_player_to_team(user: User, team_name: str):
    invites = user.invites_set.all()
    if invites.filter(name=team_name).exists():
        team = Team.objects.get(name=team_name)
        team.players.add(user)
        return {'status': 'OK'}
    else:
        return {'status': 'error', 'error': 'You are not invited to this team!'}


def create_team(user, name):
    new_team = Team.objects.create(name=name)
    new_team.save()
    user.team_role = 'COMMANDER'
    user.number_in_the_team = '1'
    user.save()
    new_team.players.add(user)
    return {'status': 'OK', 'user': user.username, 'name': name}


def leave_from_team(user):
    if user.team_set.first():
        _reset_team_role(user)
        _reset_number_in_the_team(user)
        user.team_set.first().players.remove(user)
        return {'status': 'OK'}
    else:
        return {'status': 'error', 'error': 'You haven\'t in team'}


class _User():
    def __init__(self, id, username, team_role, number_in_the_team):
        self.id = id
        self.username = username
        self.team_role = team_role
        self.number_in_the_team = number_in_the_team

    def __str__(self):
        return self.username


def _reset_team_role(user):
    user.team_role = ''
    user.save()


def _reset_number_in_the_team(user):
    user.number_in_the_team = ''
    user.save()


def _set_team_role(user, team_role):
    user.team_role = team_role
    user.save()


def _check_empty_place_in_team_roles(teammate_list):
    team_roles_query = teammate_list.values_list('team_role')
    team_roles = []
    for i, u in enumerate(team_roles_query):
        team_roles.append(team_roles_query[i][0])
    exist_c = team_roles.count('COMMANDER')
    exist_l = team_roles.count('LEGIONARY')
    exist_b = team_roles.count('BASIC')
    if exist_c > 0:
        place_c = 'FILLED'
    else:
        place_c = 'OK'
    if exist_l < 2:
        place_l = 'OK'
    else:
        place_l = 'FILLED'
    if exist_b < 3:
        place_b = 'OK'
    else:
        place_b = 'FILLED'

    return {'COMMANDER': place_c, 'LEGIONARY': place_l, 'BASIC': place_b}
