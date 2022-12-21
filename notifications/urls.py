from django.urls import path

from notifications.views import NotificationListView, NotificationSeenView,\
     NotificationSettingView, NotificationSettingsListView


urlpatterns = [
    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("seen/", NotificationSeenView.as_view(), name="notification_seen"),

    #Settings
    path("setting/site/messages/", NotificationSettingView.as_view(), name="site_message_notification_setting"),
    path("setting/site/promotions/", NotificationSettingView.as_view(), name="site_promotions_notification_setting"),
    path("setting/email/messages/", NotificationSettingView.as_view(), name="email_messages_notification_setting"),
    path("setting/email/promotions/", NotificationSettingView.as_view(), name="email_promotions_notification_setting"),
    path("settings/", NotificationSettingsListView.as_view(), name="notification_settings_list"),
]