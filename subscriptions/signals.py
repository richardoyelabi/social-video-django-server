from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Subscription, CancelledSubscription, NullifiedSubscription
from django.conf import settings

#Increase creator's subscribers number and user's active subscriptions number for new subscription
@receiver(post_save, sender=Subscription)
def update_subscriptions_numbers(sender, instance, created, **kwargs):
    if created:
        instance.subscribed_to.subscribers_number += 1 #Increase creator's subscriber number
        instance.subscriber.active_subscriptions_number += 1 #Increase account's active subscriptions number

#Move active subscription to CancelledSubscription before deleting from Subscription
@receiver(pre_delete, sender=Subscription)
def archive_subscription(sender, instance, **kwargs):
    CancelledSubscription.objects.create(
        subscribed_to=instance.subscribed_to,
        subscriber=instance.subscriber
    )
