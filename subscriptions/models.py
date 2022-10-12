from email.policy import default
from django.db import models
from django.conf import settings
from .exceptions import SubscriptionNotACreatorError
from .subscription_cut import cut
from transactions.models import Transaction

from decimal import Decimal

class Subscription(models.Model):
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="subs_subscribed_to_set", on_delete=models.CASCADE)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sub_subscriber_set", on_delete=models.CASCADE)
    time_of_subscription = models.DateTimeField(auto_now_add=True)
    fee_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd")
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)

    def save(self, *args, **kwargs):

        #Check that the account subscribed to is a creator's
        if not(self.subscribed_to.is_creator):
            raise SubscriptionNotACreatorError(f"{self.subscribed_to.username} is not a creator. Can not subscribe to non-creator account.")

        #Execute required transaction for subscription
        Transaction.objects.create(
            transaction_currency=self.fee_currency,
            amount_sent=self.fee_amount,
            sender=self.subscriber,
            platform_fee=Decimal(cut*self.fee_amount/100),
            receiver=self.subscribed_to,
            transaction_type="subscribe"
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subscriber} subscribes to {self.subscribed_to}"

class CancelledSubscription(models.Model):
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cancelled_sub_subscribed_to_set", null=True, blank=True, on_delete=models.SET_NULL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cancelled_sub_subscriber_set", null=True, blank=True, on_delete=models.SET_NULL)
    time_of_cancellation = models.DateTimeField(auto_now_add=True)
    time_of_initial_subscription = models.DateTimeField()
    fee_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd")
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)

    def __str__(self):
        return f"{self.subscriber} cancelled their subscription to {self.subscribed_to}"

class NullifiedSubscription(models.Model):
    """Model for active subscriptions that become null due to account of the subscriber or the subscribed getting deleted"""
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="nullified_sub_subscribed_to_set", null=True, blank=True, on_delete=models.SET_NULL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="nullified_sub_subscriber_set", null=True, blank=True, on_delete=models.SET_NULL)
    time_of_nullification = models.DateTimeField(auto_now_add=True)
    time_of_initial_subscription = models.DateTimeField()
    fee_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd")
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)

    def __str__(self):
        return f"{self.subscriber}'s subscription to {self.subscribed_to} has been nullified"
