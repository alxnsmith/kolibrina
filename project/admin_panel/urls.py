from django.urls import path, include
from .views import *

urlpatterns = [
    path('', AdminPanel.as_view(), name='admin_panel'),
]
