from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "time_of_transaction",
        "transaction_currency",
        "amount_sent",
        "sender",
        "platform_fee",
        "amount_received",
        "receiver",
        "transaction_type",
        "record_is_balanced",
    )

admin.site.register(Transaction, TransactionAdmin)
