from django.dispatch import receiver
from django.db.models.signals import post_save

from tips.models import Tip
from notifications.models import Notification


# Notify creator of tip
@receiver(post_save, sender=Tip)
def tip_notify(sender, instance, created, **kwargs):
    if created:
        receiver = instance.receiver
        record = instance

        Notification.notify(receiver=receiver, record=record)
