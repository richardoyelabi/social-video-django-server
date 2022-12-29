from django.db import models

from django.conf import settings
from .exceptions import SubscriptionNotACreatorError
from .subscriptions_cut import cut as float_cut
from transactions.models import Transaction
from transactions.currency_convert import convert_currency
from transactions.exceptions import TransactionInsufficientBalanceError

from decimal import Decimal


class SubscriptionTransaction(models.Model):
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sub_transaction_subscribed_to_set", null=True, blank=True, on_delete=models.SET_NULL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sub_transaction_subscriber_set", null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    fee_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd")
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)
    subscription = models.ForeignKey("subscriptions.Subscription", related_name="transaction", on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):

        #Convert monetary values to decimal
        cut = Decimal(float_cut)
        self.fee_amount = Decimal(self.fee_amount)

        source_currency, source_amount = self.fee_currency, self.fee_amount

        #Store currency choices in simple list
        currencies = [i[0] for i in Transaction.currency_choices]
        currencies.remove(self.fee_currency)
        currencies.insert(0, self.fee_currency)

        for currency in currencies:
            # Try to pay for subscription with each of subscriber's wallets 
            # until one has enough money to pay.
            # Otherwise, raise an exception.

            #Convert fee_amount to destination currency if needed
            self.fee_amount = convert_currency(
                source = source_currency,
                target = currency,
                amount = source_amount
            )

            self.fee_currency = currency

            try:
                Transaction.objects.create(
                    transaction_currency=self.fee_currency,
                    amount_sent=self.fee_amount,
                    sender=self.subscriber,
                    platform_fee=cut*self.fee_amount/100,
                    receiver=self.subscribed_to,
                    transaction_type="subscribe"
                )
                break
            except TransactionInsufficientBalanceError:
                if currencies.index(currency) == len(currencies)-1:
                    raise

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subscriber} paid subscription fee to {self.subscribed_to}"


class Subscription(models.Model):
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="subs_subscribed_to_set", on_delete=models.CASCADE)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sub_subscriber_set", on_delete=models.CASCADE)
    time_of_subscription = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        creator_account =  self.subscribed_to

        #Check that the account subscribed to is a verified creator's
        if not(creator_account.is_creator):
            raise SubscriptionNotACreatorError(f"{creator_account.username} is not a creator. Can not subscribe to non-creator account.")
        if not(creator_account.creatorinfo.is_verified):
            raise SubscriptionNotACreatorError(f"{creator_account.username} is not a verified creator.")

        #Get subscription fee
        creator_info = creator_account.creatorinfo
        fee_currency, fee_amount = (creator_info.subscription_fee_currency, creator_info.subscription_fee_amount)

        try:
            SubscriptionTransaction.objects.create(
                subscribed_to = self.subscribed_to,
                subscriber = self.subscriber,
                fee_currency = fee_currency,
                fee_amount = fee_amount
            )
        except TransactionInsufficientBalanceError:
            raise

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subscriber} subscribes to {self.subscribed_to}"


class CancelledSubscription(models.Model):
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cancelled_sub_subscribed_to_set", null=True, blank=True, on_delete=models.SET_NULL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cancelled_sub_subscriber_set", null=True, blank=True, on_delete=models.SET_NULL)
    time_of_cancellation = models.DateTimeField(auto_now_add=True)
    time_of_initial_subscription = models.DateTimeField()

    def __str__(self):
        return f"{self.subscriber} cancelled their subscription to {self.subscribed_to}"


class NullifiedSubscription(models.Model):
    """Model for active subscriptions that become null due to account of the subscriber or the subscribed getting deleted"""
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="nullified_sub_subscribed_to_set", null=True, blank=True, on_delete=models.SET_NULL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="nullified_sub_subscriber_set", null=True, blank=True, on_delete=models.SET_NULL)
    time_of_nullification = models.DateTimeField(auto_now_add=True)
    time_of_initial_subscription = models.DateTimeField()

    def __str__(self):
        return f"{self.subscriber}'s subscription to {self.subscribed_to} has been nullified"
