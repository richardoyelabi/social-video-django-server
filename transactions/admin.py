from django.contrib import admin
from .models import Transaction, WithdrawalRequest, Withdrawal


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
        "transaction_type",
        "transaction_currency",
        "amount_sent",
        "receiver",
    )


class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "creator",
        "handled",
    )

    fields = ("handled",)


class WithdrawalAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "creator",
        "wallet",
        "amount",
        "timestamp",
    )

    fields = (
        "creator",
        "wallet",
        "amount",
    )


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)
admin.site.register(Withdrawal, WithdrawalAdmin)
