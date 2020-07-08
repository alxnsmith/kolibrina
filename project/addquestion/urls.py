from django.urls import path
from . import views

urlpatterns = [
    path('', views.addQuestion, name='add-question'),
    path('get-themes', views.getThemes, name='getTheme')
]