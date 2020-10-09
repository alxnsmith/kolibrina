from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.navigate, name='questions'),
    path('api', views.questions_api, name='questions_api'),
    path('add-question', views.add_question, name='add-question'),
    path('add-tournament-week', views.add_tournament_week, name='add-tournament-week'),
    path('add-theme-blocks-marafon-week', login_required(views.AddThemeBlocksMarafonWeek.as_view(), login_url='login'), name='add_theme_blocks_marafon_week'),
]