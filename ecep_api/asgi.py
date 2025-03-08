# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notifications.routing  # Importer les routes WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifications.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notifications.routing.websocket_urlpatterns  # Assurez-vous d'avoir défini les URL WebSocket
        )
    ),
})
