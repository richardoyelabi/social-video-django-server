from django.urls import path

from channels.routing import URLRouter

from chats.routing import websocket_urlpatterns as chat_routing
from posts.routing import websocket_urlpatterns as post_routing
from notifications.routing import websocket_urlpatterns as notification_routing

websocket_urlpatterns = [
    path("ws/chat/", URLRouter(chat_routing)),
    path("ws/post/", URLRouter(post_routing)),
    path("ws/notification/", URLRouter(notification_routing)),
]
