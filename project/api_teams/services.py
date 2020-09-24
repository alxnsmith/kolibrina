from django.core.exceptions import ObjectDoesNotExist
from .models import Team
from userK.models import CustomUser, InviteToTeam


def set_number_on_the_team(username, number):
    user = CustomUser.objects.get(username=username)
    team_object = Team.objects.get(team_name=user.team)
    occupied_player_numbers = [i['number_in_the_team'] for i in team_object.customuser_set.values('number_in_the_team')]
    if occupied_player_numbers.__contains__(number):
        return {'status': 'error', 'error': 'This number is occupied'}
    user.number_in_the_team = number
    user.save()
    return {'status': 'OK'}


def del_player_from_team(player, team):
    exists = CustomUser.objects.filter(username=player).exists()
    if exists:
        player = CustomUser.objects.get(username=player)
        if player.team == team:
            player.team = None
            _reset_number_in_the_team(player)
            _reset_team_role(player)
            return {'status': 'OK'}
        else:
            return {'status': 'error', 'error': "Player is not a member of this team"}
    else:
        return {'status': 'error', 'error': 'There is no such user!'}


def delete_team(user):
    team_role = user.team_role
    team_name = user.team
    if Team.objects.filter(team_name=team_name).exists():
        team = Team.objects.get(team_name=team_name)
        if team.customuser_set.filter(username=user.username).exists():
            if team_role == 'COMMANDER':
                _reset_team_role(user)
                _reset_number_in_the_team(user)
                team.delete()
                return {'status': 'OK'}


def add_player_to_invite_list(user_id, team_id):
    exists = InviteToTeam.objects.filter(team=team_id, user=user_id).exists()
    if not exists:
        team = Team.objects.get(id=team_id)
        user = CustomUser.objects.get(id=user_id)
        InviteToTeam.objects.create(team=team, user=user)
        return {'status': 'OK'}
    return {'status': 'error', 'error': 'This invitation is already there'}


def get_team_info(team, user):
    try:
        team_object = Team.objects.get(team_name=team)
    except ObjectDoesNotExist:
        return {'Error': 'Нет такой команды'}
    players_list = list(team_object.customuser_set.values('id', 'username', 'team_role', 'number_in_the_team'))
    players = _create_dict_with_user_models(players_list)
    if not players['list'].__contains__(str(user)):
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
    teammate_list = user.team.customuser_set.all()
    if user.team_role == 'COMMANDER':
        if put.__contains__('username'):
            if teammate_list.filter(username=put['username']).exists():
                user = teammate_list.get(username=put['username'])
    empty_places_list = _check_empty_place_in_team_roles(teammate_list=teammate_list)
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


def join_player_to_team(user, team_name):
    user = CustomUser.objects.get(username=user.username)
    invited = user.invitetoteam_set.all()
    if invited.filter(team__team_name=team_name).exists():
        team = Team.objects.get(team_name=team_name)
        user.team = team
        user.save()
        return {'status': 'OK'}
    else:
        return {'status': 'error', 'error': 'You are not invited to this team!'}


def create_team(user, team_name):
    new_team = Team.objects.create(team_name=team_name)
    new_team.save()
    user.team_role = 'COMMANDER'
    user.number_in_the_team = '1'
    user.team = new_team
    user.save()
    return {'status': 'OK', 'user': user.username, 'team_name': team_name}


def leave_from_team(user):
    if user.team:
        _reset_team_role(user)
        _reset_number_in_the_team(user)
        user.team = None
        user.save()
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
    exist_l = team_roles.count('LEGIONARY')
    exist_b = team_roles.count('BASIC')
    if exist_l < 2:
        place_l = 'OK'
    else:
        place_l = 'FILLED'
    if exist_b < 3:
        place_b = 'OK'
    else:
        place_b = 'FILLED'

    return {'LEGIONARY': place_l, 'BASIC': place_b}