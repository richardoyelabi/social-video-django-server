from django.contrib import admin
from .models import Purchase, CancelledPurchase, NullifiedPurchase

class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "video",
        "time_of_purchase",
    )

class CancelledPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "video",
        "time_of_cancellation",
        "time_of_initial_purchase",
    )

class NullifiedPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "video",
        "time_of_nullification",
        "time_of_initial_purchase",
    )

admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(CancelledPurchase, CancelledPurchaseAdmin)
admin.site.register(NullifiedPurchase, NullifiedPurchaseAdmin)
