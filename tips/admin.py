from django.contrib import admin
from tips.models import Tip

class TipAdmin(admin.ModelAdmin):
    list_display = (
        "sender",
        "receiver",
        "created",
        "fee_currency",
        "fee_amount",
    )


admin.site.register(Tip, TipAdmin)
