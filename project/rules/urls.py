from django.urls import path
from .views import rules

urlpatterns = [
    path('', rules, name='rules')
]