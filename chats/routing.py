from django.urls import path

from chats.consumers import (
    OnlineOfflineConsumer,
    WatchStatusConsumer,
    InboxConsumer,
    MessageConsumer,
)

websocket_urlpatterns = [
    path("status/", OnlineOfflineConsumer.as_asgi()),
    path("watch-status/<uuid:public_id>/", WatchStatusConsumer.as_asgi()),
    path("inbox/", InboxConsumer.as_asgi()),
    path("<uuid:public_id>/", MessageConsumer.as_asgi()),
]
