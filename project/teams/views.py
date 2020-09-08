from django.http import JsonResponse
from django.shortcuts import HttpResponse
import json

from .services import get_team_info


def team_api(request):
    team = 'Бобры'
    if request.method == 'GET':
        return JsonResponse(_get_team_info(team))
    elif request.method == 'POST':
        return JsonResponse({"method": 'POST',
                             "status": 'OK',
                             })
    else:
        return HttpResponse("Error")


def _get_team_info(team):
    return get_team_info(team=team)


def _add_player_to_team(request):
    return JsonResponse("good")
