from .models import Team
import json


def add_player_to_team(username, team):
    pass


def add_invite_to_a_team(username, team):
    pass


def add_set_team_number_for_player(username, number):
    pass


def get_team_info(team):
    players = list(Team.objects.get(team_name=team).customuser_set.values('id',
                                                                          'username',
                                                                          'team_role',
                                                                          'number_in_the_team'))
    data = {
        'team': team,
        'players': players,
        'score': 'score',
        'last_game_date': 'last_game_date',
    }
    return data
