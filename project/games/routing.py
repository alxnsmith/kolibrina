from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/tournament-week-<str:tournament_name>/', consumers.TournamentWeek.as_asgi()),
    re_path(r'ws/marafon-week/$', consumers.MarafonWeek.as_asgi()),
]
