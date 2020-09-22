from django.urls import path
from . import views

urlpatterns = [
    path('', views.navigate, name='questions'),
    path('api', views.questions_api, name='questions_api'),
    path('add-question', views.addQuestion, name='add-question'),
    path('add-tournament-week', views.add_tournament_week, name='add-tournament-week'),
]