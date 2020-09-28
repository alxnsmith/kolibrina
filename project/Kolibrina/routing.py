from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import channel_common.routing
import games.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns +
            channel_common.routing.websocket_urlpatterns +
            games.routing.websocket_urlpatterns
        )
    ),
})
