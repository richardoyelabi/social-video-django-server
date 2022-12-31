from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Subscription, CancelledSubscription, NullifiedSubscription
from notifications.models import Notification
from django_celery_beat.models import PeriodicTask


# Delete subscription task on subscription delete
@receiver(pre_delete, sender=Subscription)
def delete_sub_task(sender, instance, **kwargs):
    try:
        instance.task.delete()
    except PeriodicTask.DoesNotExist:
        pass


# Update subscription data for each new subscription
@receiver(post_save, sender=Subscription)
def increase_subscriptions_numbers(sender, instance, created, **kwargs):

    #Increase creator's subscribers number and user's active subscriptions number for each new subscription instance
    if created:
        instance.subscribed_to.creatorinfo.subscribers_number += 1
        instance.subscriber.active_subscriptions_number += 1
        instance.subscribed_to.creatorinfo.save(update_fields=["subscribers_number"])
        instance.subscriber.save(update_fields=["active_subscriptions_number"])


# Update subscription data for each new unsubscription
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
        subscriber=instance.subscriber,
        time_of_initial_subscription=instance.time_of_subscription
    )


# Notify creator of subscription
@receiver(post_save, sender=Subscription)
def subscription_notify(sender, instance, created, **kwargs):

    if created:

        receiver = instance.subscribed_to
        record = instance

        Notification.notify(receiver=receiver, record=record)