from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/tournament-week-<str:tournament_name>/', consumers.TournamentWeek),
]
