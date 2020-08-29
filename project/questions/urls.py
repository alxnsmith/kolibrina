from django.urls import path
from . import views

urlpatterns = [
    path('', views.navigate, name='questions'),
    path('add-question', views.addQuestion, name='add-question'),
    path('get-themes/', views.getThemes, name='getTheme')
]