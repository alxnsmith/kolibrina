from django.urls import path
from . import views

urlpatterns = [
    path('', views.train, name='train'),
    path('result-games/', views.win_lose, name='result-games'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('clarify-question/', views.clarify_question, name='clarify-question'),
    path('api-games/', views.apiGame, name='apiGame'),
]
