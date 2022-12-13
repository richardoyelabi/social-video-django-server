from django.contrib import admin
from notifications.models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "public_id",
        "receiver",
        "record",
        "timestamp"
    )

admin.site.register(Notification, NotificationAdmin)