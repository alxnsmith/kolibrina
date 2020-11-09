import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kolibrina.settings')
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import channel_common.routing
import chat.routing
import games.routing
import admin_panel.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns +
            channel_common.routing.websocket_urlpatterns +
            games.routing.websocket_urlpatterns +
            admin_panel.routing.websocket_urlpatterns
        )
    )
})
