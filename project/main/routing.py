from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/text-info-<game_type>/', consumers.TextInfoConsumer.as_asgi()),
]
