from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('login/', views.loginK, name='login'),
    path('logout/', views.logoutK, name='logout'),
]