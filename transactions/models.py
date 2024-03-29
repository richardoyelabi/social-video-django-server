from django.conf import settings
from django.db import models

import uuid

from transactions.exceptions import (
    TransactionInputError,
    TransactionInsufficientBalanceError,
)


class Transaction(models.Model):
    currency_choices = [
        ("usd", "United States Dollar"),
        ("btc", "Bitcoin"),
    ]
    transaction_types = [
        ("deposit", "Deposit"),
        ("withdraw", "Withdrawal"),
        ("subscribe", "Subscription payment"),
        ("buy", "Video purchase"),
        ("tip", "Creator tip"),
        ("request", "Special request payment"),
    ]

    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    time_of_transaction = models.DateTimeField(auto_now_add=True)
    transaction_currency = models.CharField(max_length=3, choices=currency_choices)
    amount_sent = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="debit_transactions",
    )
    platform_fee = models.DecimalField(max_digits=100, decimal_places=50, default=0)
    amount_received = models.DecimalField(
        max_digits=100, decimal_places=50, default=0.00
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="credit_transactions",
    )
    transaction_type = models.CharField(max_length=10, choices=transaction_types)
    record_is_balanced = models.BooleanField(default=False)

    @classmethod
    def get_wallet(self, account, target_wallet):
        if target_wallet == "usd":
            wallet = account.usd_wallet_balance
        elif target_wallet == "btc":
            wallet = account.btc_wallet_balance
        return wallet

    def take_from_wallet(self, currency, amount):
        if self.sender:
            if amount > 0:
                wallet = self.get_wallet(self.sender, currency)
                if wallet >= amount:
                    wallet -= amount

                    # Update Wallet
                    if currency == "usd":
                        self.sender.usd_wallet_balance = wallet
                        self.sender.save(update_fields=["usd_wallet_balance"])
                    elif currency == "btc":
                        self.sender.btc_wallet_balance = wallet
                        self.sender.save(update_fields=["btc_wallet_balance"])

                else:
                    raise TransactionInsufficientBalanceError(
                        f"There isn't enough money in your wallet to complete this transaction."
                    )
            elif amount < 0:
                raise TransactionInputError(
                    "You've entered a negative input as amount_sent."
                )

    def add_to_wallet(self, currency, amount):
        if self.receiver:
            if amount > 0:
                wallet = self.get_wallet(self.receiver, currency)
                wallet += amount

                # Update Wallet
                if currency == "usd":
                    self.receiver.usd_wallet_balance = wallet
                    self.receiver.save(update_fields=["usd_wallet_balance"])
                elif currency == "btc":
                    self.receiver.btc_wallet_balance = wallet
                    self.receiver.save(update_fields=["btc_wallet_balance"])

            elif amount < 0:
                raise TransactionInputError(
                    "You've entered a negative input as amount_received. This can be as a result of platform_fee exceeding amount_sent."
                )

    def is_record_balanced(self):
        self.record_is_balanced = (
            self.amount_sent == self.amount_received + self.platform_fee
        )

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.take_from_wallet(self.transaction_currency, self.amount_sent)
            self.amount_received = self.amount_sent - self.platform_fee
            self.add_to_wallet(self.transaction_currency, self.amount_received)
            self.is_record_balanced()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.public_id}"


class WithdrawalRequest(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="withdrawal_requests",
    )
    handled = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WithdrawalRequest {self.public_id}"


class Withdrawal(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="withdrawals",
    )
    wallet = models.CharField(
        max_length=3, choices=Transaction.currency_choices, default="usd"
    )
    amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        Transaction.objects.create(
            transaction_currency=self.wallet,
            amount_sent=self.amount,
            sender=self.creator,
            platform_fee=0,
            receiver=None,
            transaction_type="withdraw",
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Withdrawal {self.public_id}"
