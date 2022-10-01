from django.db import models
from django.conf import settings
from accounts.models import CreatorInfo

class Subscription(models.Model):
    subscribed_to = models.ForeignKey(CreatorInfo, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_of_subscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscriber} subscribes to {self.subscribed_to}"

class CancelledSubscription(models.Model):
    subscribed_to = models.ForeignKey(CreatorInfo, null=True, blank=True, on_delete=models.SET_NULL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    time_of_cancellation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscriber} cancelled their subscription to {self.subscribed_to}"

class NullifiedSubscription(models.Model):
    """Model for active subscriptions that become null due to account of the subscriber or the subscribed getting deleted"""
    subscribed_to = models.ForeignKey(CreatorInfo, null=True, blank=True, on_delete=models.SET_NULL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    time_of_nullification = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscriber}'s subscription to {self.subscribed_to} has been nullified"
