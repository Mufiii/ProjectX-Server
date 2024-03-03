from django.urls import re_path
from chatroom.consumers import ChatConsumer
from channels.routing import URLRouter

# This file defines the routing configuration for handling WebSocket connections.


websocket_urlpatterns = [
	re_path(
		r'ws/users/(?P<userId>\w+)/chat/$',
		ChatConsumer.as_asgi()
	),
]



# websocket_urlpatterns = [
#         re_path(
            
#             r"ws/chat/(?P<room_name>\w+)/$", 
#             ChatConsumer.as_asgi()
#         ),
# ]

