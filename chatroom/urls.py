from django.urls import include, path
from .views import ListMessages
from chatroom.routing import websocket_urlpatterns

urlpatterns = [
    # path("ws/", include(websocket_urlpatterns)),
    path('messages/',ListMessages.as_view())
]