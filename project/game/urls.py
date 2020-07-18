from django.urls import path
from . import views

urlpatterns = [
    path('', views.train, name='train'),
    path('result-game/', views.win_lose, name='result-game'),
    path('tournaments/', views.tournaments, name='tournaments'),
]
