from django.contrib import admin
from .models import SpecialRequest, MessagePurchase


class SpecialRequestAdmin(admin.ModelAdmin):
    list_display = (
        "request_by",
        "request_to",
        "request",
        "created",
    )


class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "video_message",
        "created",
        "fee_currency",
        "fee_amount",
    )


admin.site.register(SpecialRequest, SpecialRequestAdmin)
admin.site.register(MessagePurchase, PurchaseAdmin)
