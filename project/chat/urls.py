from django.urls import path
from .views import Chat
from . import api

urlpatterns = [
    path('', Chat.as_view(), name='chat'),
    path('api/', api.get_last_messages, name='chatAPI'),
]
