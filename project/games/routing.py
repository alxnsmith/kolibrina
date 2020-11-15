from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/tournament-week-<str:tournament_shortname>/', consumers.TournamentWeek.as_asgi()),
]
