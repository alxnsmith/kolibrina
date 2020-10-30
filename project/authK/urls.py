from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logoutK, name='logout'),
]