from django.urls import path, include

from channels.routing import URLRouter

from chats.routing import websocket_urlpatterns as chat_routing
#from posts.routing import websocket_urlpatterns as post_routing

websocket_urlpatterns = [
    path("ws/chat/", URLRouter(chat_routing)),
    #path("ws/post/", include("posts.routing")),
]