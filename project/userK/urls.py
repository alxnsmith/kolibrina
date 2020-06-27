from django.urls import path
from . import views

urlpatterns = [
    path('useraccount', views.account),
]