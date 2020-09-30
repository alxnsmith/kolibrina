from django.urls import path
from . import views

urlpatterns = [
    path('', views.train, name='train'),
    path('tournament-week', views.tournament_week, name='tournament-week'),
    path('result-games/', views.win_lose, name='result-game'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('clarify-question/', views.clarify_question, name='clarify-question'),
    path('api-train/', views.api_train, name='api_train'),
]
