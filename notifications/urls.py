from django.urls import path

from notifications.views import NotificationListView, NotificationSeenView


urlpatterns = [
    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("seen/", NotificationSeenView.as_view(), name="notification_seen"),
]