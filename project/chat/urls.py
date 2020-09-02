from django.urls import path
from .views import chat
from . import api

urlpatterns = [
    path('', chat, name='chat'),
    path('api/', api.get_last_messages, name='chatAPI'),
]
