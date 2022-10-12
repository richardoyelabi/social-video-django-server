from django.contrib import admin
from .models import Subscription, CancelledSubscription, NullifiedSubscription

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "subscribed_to",
        "subscriber",
        "time_of_subscription",
        "fee_currency",
        "fee_amount",
    )

class CancelledSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "subscribed_to",
        "subscriber",
        "time_of_cancellation",
        "time_of_initial_subscription",
        "fee_currency",
        "fee_amount",
    )

class NullifiedSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "subscribed_to",
        "subscriber",
        "time_of_nullification",
        "time_of_initial_subscription",
        "fee_currency",
        "fee_amount",
    )

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(CancelledSubscription, CancelledSubscriptionAdmin)
admin.site.register(NullifiedSubscription, NullifiedSubscriptionAdmin)
