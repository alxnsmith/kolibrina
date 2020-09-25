from django.http import JsonResponse, QueryDict
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from . import services
from api_teams import services as team_services


@csrf_exempt
def team_api(request):
    user = request.user

    if request.method == 'GET':
        get = request.GET
        if 'event' in get:
            event = get['event']
            if event == 'get_team_info':
                return JsonResponse(_get_team_info(get['team'], user))
            elif event == 'set_number_in_the_team':
                return JsonResponse(_set_team_number_for_player(user, get.number))
            else:
                return JsonResponse({'error': 'Error! Unknown event.'})
        else:
            return JsonResponse({'status': 'ERROR! Need "event".'})

    elif request.method == 'POST':
        post = json.loads(request.body)
        if 'event' in post:
            event = post['event']
            if event == 'add_player_to_invite_list':
                return _add_player_to_invite_list(post['player_id'], user.team.id)
            elif event == 'create_team':
                return _create_team(user, post['team_name'])
            else:
                return JsonResponse({'error': 'Error! Unknown event.'})
        else:
            return JsonResponse({'status': 'ERROR! Need "event".'})

    elif request.method == 'DELETE':
        data = json.loads(request.body)
        if 'event' in data:
            event = data['event']
            if event == 'delete_player_from_team':
                result = services.del_player_from_team(team=user.team, player=data['player'])
                return JsonResponse(result)
            elif event == 'delete_team':
                result = services.delete_team(user)
                return JsonResponse(result)
            else:
                return JsonResponse({'error': 'Error! Unknown event.'})
        else:
            return JsonResponse({'status': 'ERROR! Need "event".'})

    elif request.method == 'PUT':
            put = json.loads(request.body)
            if 'event' in put:
                event = put['event']
                if event == 'set_number_in_the_team':
                    return _set_team_number_for_player(put, user)
                elif event == 'set_team_role':
                    return _set_team_role(user, put)
                elif event == 'join_to_team':
                    return JsonResponse(services.join_player_to_team(user=user, team_name=put['team_name']))
                elif event == 'leave_from_team':
                    return JsonResponse(services.leave_from_team(user=user))
                else:
                    return JsonResponse({'error': 'Error! Unknown event.'})
            else:
                return JsonResponse({'status': 'ERROR! Need "event".'})
    else:
        return HttpResponse("Error")


def _set_team_role(user, put):
    result = services.set_player_team_role(user=user, put=put)
    return JsonResponse(result)


def _create_team(user, team_name):
    result = team_services.create_team(user=user, team_name=team_name)
    return JsonResponse(result)


def _get_team_info(team, user):
    team_info = services.get_team_info(team=team, user=user)
    return team_info


def _add_player_to_invite_list(user_id, team_id):
    result = services.add_player_to_invite_list(user_id, team_id)
    return JsonResponse(result)


def _set_team_number_for_player(put, user):
    number = str(put['number'])
    if services.set_number_on_the_team(user, number)['status'] == 'OK':
        return JsonResponse({'status': 'set_number_in_the_team'})
    return JsonResponse({'status': 'Error! Need "number"'})
