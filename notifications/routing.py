from django.urls import path

from notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    path("connect/", NotificationConsumer.as_asgi(), name="notification_connect"),
]