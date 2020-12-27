from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AdminPanel.as_view(), name='admin_panel'),
]
