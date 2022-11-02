from django.contrib import admin
from .models import Purchase, CancelledPurchase, NullifiedPurchase

class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "video_post",
        "time_of_purchase",
        "fee_currency",
        "fee_amount",
    )

class CancelledPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "video_post",
        "time_of_cancellation",
        "time_of_initial_purchase",
        "fee_currency",
        "fee_amount",
    )

class NullifiedPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "video_post",
        "time_of_nullification",
        "time_of_initial_purchase",
        "fee_currency",
        "fee_amount",
    )

admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(CancelledPurchase, CancelledPurchaseAdmin)
admin.site.register(NullifiedPurchase, NullifiedPurchaseAdmin)
