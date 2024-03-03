
import os

# 👇 1. Update the below import lib
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
from chatroom.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from chatroom.routing import websocket_urlpatterns
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProjectX.settings")
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
	'http': django_asgi_app,
	'websocket': AllowedHostsOriginValidator(
		JWTAuthMiddlewareStack(
			URLRouter(websocket_urlpatterns)
		)
	)
})