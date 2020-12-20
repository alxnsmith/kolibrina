from django.contrib.auth.decorators import login_required
from django.urls import path, include

from .views import tournament_week, train, win_lose, tournaments, clarify_question, api_train, RegisterToGame

urlpatterns = [
    path('tournaments/', tournaments, name='tournaments'),
    path('register-to-game/', RegisterToGame.as_view(), name='register_to_game'),

    path('', train, name='train'),
    path('api-train/', api_train, name='api_train'),

    path('tournament-week', login_required(tournament_week), name='tournament-week'),
    path('marafon/', include('marathon.urls')),

    path('clarify-question/', login_required(clarify_question), name='clarify-question'),
    path('result-games/', win_lose, name='result-game'),
]
