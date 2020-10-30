from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from . import views

urlpatterns = [
    path('', views.navigate, name='questions'),
    path('api/', csrf_exempt(views.QuestionAPI.as_view()), name='questions_api'),
    path('add-question/', login_required(views.AddQuestion.as_view(), login_url='login'), name='add-question'),
    path('add-tournament-week/', views.add_tournament_week, name='add-tournament-week'),
    path('add-theme-blocks-marafon-week/', login_required(views.AddThemeBlocksMarafonWeek.as_view(), login_url='login'), name='add_theme_blocks_marafon_week'),
]