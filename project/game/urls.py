from django.urls import path
from . import views

urlpatterns = [
    path('', views.train, name='train'),
    path('win/', views.win_lose, name='win'),
    path('tournaments/', views.tournaments, name='tournaments'),
]
