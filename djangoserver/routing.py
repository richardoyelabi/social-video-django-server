from django.urls import path

from channels.routing import URLRouter

from chats.routing import websocket_urlpatterns as chat_routing
from posts.routing import websocket_urlpatterns as post_routing

websocket_urlpatterns = [
    path("ws/chat/", URLRouter(chat_routing)),
    path("ws/post/", URLRouter(post_routing)),
]