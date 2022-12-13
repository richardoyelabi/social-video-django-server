from django.dispatch import receiver
from django.db.models.signals import post_save

from special_requests.models import SpecialRequest, MessagePurchase
from notifications.models import Notification


#Notify creator of special request
@receiver(post_save, sender=SpecialRequest)
def request_notify(sender, instance, created, **kwargs):

    if created:

        receiver = instance.request_to
        record = instance

        Notification.notify(receiver=receiver, record=record)


#Notify creator of message purchase
@receiver(post_save, sender=MessagePurchase)
def message_purchase_notify(sender, instance, created, **kwargs):

    if created:

        receiver = instance.video_message.user
        record = instance

        Notification.notify(receiver=receiver, record=record)