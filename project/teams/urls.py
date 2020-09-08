from django.urls import path
from . import views


urlpatterns = [
    path('', views.team_api, name='team_api'),
]
