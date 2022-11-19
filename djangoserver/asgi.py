"""
ASGI config for djangoserver project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoserver.settings')

django_asgi_app = get_asgi_application()

from . import routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels_auth_token_middlewares.middleware import DRFAuthTokenMiddleware

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": DRFAuthTokenMiddleware(
        URLRouter(
            routing.websocket_urlpatterns
        ),
    ),
    
})
