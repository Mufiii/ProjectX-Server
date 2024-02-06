from django.urls import re_path
from chatroom.consumers import ChatConsumer
from channels.routing import URLRouter

websocket_urlpatterns = [
        re_path(
            
            r"ws/chat/(?P<room_name>\w+)/$", 
            ChatConsumer.as_asgi()
        ),
]

