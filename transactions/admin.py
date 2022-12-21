from django.contrib import admin
from .models import Transaction, WithdrawalRequest


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

    fields = (
        "transaction_currency",
        "amount_sent",
        "sender",
    )


class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "creator",
        "handled",
    )

    fields = (
        "handled",
    )


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)