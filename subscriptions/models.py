from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from django.conf import settings
from .exceptions import SubscriptionNotACreatorError
from .subscriptions_cut import cut as float_cut
from transactions.models import Transaction
from transactions.currency_convert import convert_currency
from transactions.exceptions import TransactionInsufficientBalanceError

from decimal import Decimal
import uuid
import json


# Number of days before subscription expires
validity_period = 30 #days


class SubscriptionTransaction(models.Model):
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sub_transaction_subscribed_to_set", null=True, blank=True, on_delete=models.SET_NULL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sub_transaction_subscriber_set", null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    fee_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd")
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)

    def save(self, *args, **kwargs):

        #Get subscription fee
        creator_info = self.subscribed_to.creatorinfo
        self.fee_currency, self.fee_amount = (creator_info.subscription_fee_currency, creator_info.subscription_fee_amount)

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
            # until one wallet has enough money to pay.
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
    task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):

        creator_account =  self.subscribed_to

        #Check that the account subscribed to is a verified creator's
        if not(creator_account.is_creator):
            raise SubscriptionNotACreatorError(f"{creator_account.username} is not a creator. Can not subscribe to non-creator account.")
        if not(creator_account.creatorinfo.is_verified):
            raise SubscriptionNotACreatorError(f"{creator_account.username} is not a verified creator.")

        try:
            SubscriptionTransaction.objects.create(
                subscribed_to = self.subscribed_to,
                subscriber = self.subscriber
            )
        except TransactionInsufficientBalanceError:
            raise

        if not PeriodicTask.objects.filter(
            name = f"subscription_{self.subscribed_to.public_id}_{self.subscriber.public_id}"
        ).exists():

            schedule, created = IntervalSchedule.objects.get_or_create(every=validity_period, period=IntervalSchedule.DAYS)

            self.task = PeriodicTask.objects.create(
                name = f"subscription_{self.subscribed_to.public_id}_{self.subscriber.public_id}",
                task = "subscriptions.tasks.process_sub_transaction",
                interval = schedule,
                args=json.dumps([self.subscribed_to.id, self.subscriber.id]),
            )

        else:
            self.task = PeriodicTask.objects.get(
                name = f"subscription_{self.subscribed_to.public_id}_{self.subscriber.public_id}"
            )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        try:
            self.task.delete() # this results in super().delete() call due to cascading delete
        except PeriodicTask.DoesNotExist:
            pass

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
