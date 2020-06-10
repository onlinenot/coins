from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator


from main.consumers import CoinsConsumer
#from chat.consumers import AdminChatConsumer, PublicChatConsumer
#from aprs_news.consumers import APRSNewsConsumer

application = ProtocolTypeRouter({

    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                url("", CoinsConsumer),
            ])
        )
    ),

})
