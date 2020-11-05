import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import chat.routing
import channel_common.routing
import games.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Kolibrina.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns +
            channel_common.routing.websocket_urlpatterns +
            games.routing.websocket_urlpatterns
        )
    )
})
