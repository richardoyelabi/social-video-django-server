from django.contrib import admin
from .models import MessagePurchase


class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "video_message",
        "created",
        "fee_currency",
        "fee_amount",
    )

admin.site.register(MessagePurchase, PurchaseAdmin)
