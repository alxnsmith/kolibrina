from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/tournament-week-<str:tournament_name>/', consumers.TournamentWeek),
    re_path(r'ws/marafon-week/$', consumers.MarafonWeek),
]
