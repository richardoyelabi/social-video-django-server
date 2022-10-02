from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Subscription, CancelledSubscription, NullifiedSubscription
from django.conf import settings

@receiver(post_save, sender=Subscription)
def increase_subscriptions_numbers(sender, instance, created, **kwargs):

    #Increase creator's subscribers number and user's active subscriptions number for each new subscription instance
    if created:
        instance.subscribed_to.creatorinfo.subscribers_number += 1
        instance.subscriber.active_subscriptions_number += 1
        instance.subscribed_to.creatorinfo.save(update_fields=["subscribers_number"])
        instance.subscriber.save(update_fields=["active_subscriptions_number"])

@receiver(pre_delete, sender=Subscription)
def decrease_subscriptions_numbers_and_archive_subscription(sender, instance, **kwargs):
    
    #Decrease creator's subscribers number and user's active subscriptions number for each deleted subscription instance
    instance.subscribed_to.creatorinfo.subscribers_number -= 1
    instance.subscriber.active_subscriptions_number -= 1
    instance.subscribed_to.creatorinfo.save(update_fields=["subscribers_number"])
    instance.subscriber.save(update_fields=["active_subscriptions_number"])

    #Move active subscription to CancelledSubscription before deleting from Subscription
    CancelledSubscription.objects.create(
        subscribed_to=instance.subscribed_to,
        subscriber=instance.subscriber
    )

