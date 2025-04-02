from django.urls import re_path
from . import consumers
from .consumers import ChatConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/chat/", consumers.ChatConsumer.as_asgi()),
    ])
})


application = ProtocolTypeRouter({
    "websocket": JWTAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    )
})

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<session_id>\w+)/$', ChatConsumer.as_asgi()),
]