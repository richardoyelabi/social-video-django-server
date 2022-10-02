from django.db import models
from django.conf import settings
from .exceptions import SubscriptionNotACreatorError

class Subscription(models.Model):
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="subs_subscribed_to_set", on_delete=models.CASCADE)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sub_subscriber_set", on_delete=models.CASCADE)
    time_of_subscription = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.subscribed_to.is_creator:
            super().save(*args, **kwargs)
        else:
            raise SubscriptionNotACreatorError(f"{self.subscribed_to.username} is not a creator. Can not subscribe to non-creator account.")

    def __str__(self):
        return f"{self.subscriber} subscribes to {self.subscribed_to}"

class CancelledSubscription(models.Model):
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cancelled_sub_subscribed_to_set", null=True, blank=True, on_delete=models.SET_NULL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cancelled_sub_subscriber_set", null=True, blank=True, on_delete=models.SET_NULL)
    time_of_cancellation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscriber} cancelled their subscription to {self.subscribed_to}"

class NullifiedSubscription(models.Model):
    """Model for active subscriptions that become null due to account of the subscriber or the subscribed getting deleted"""
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="nullified_sub_subscribed_to_set", null=True, blank=True, on_delete=models.SET_NULL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="nullified_sub_subscriber_set", null=True, blank=True, on_delete=models.SET_NULL)
    time_of_nullification = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscriber}'s subscription to {self.subscribed_to} has been nullified"
