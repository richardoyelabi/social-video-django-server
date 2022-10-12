from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Purchase, CancelledPurchase, NullifiedPurchase

#Update purchase data for each new purchase
@receiver(post_save, sender=Purchase)
def increase_purchased_videos_number(sender, instance, created, **kwargs):

    #Increase user's purchased videos number for each new video purchase
    if created:
        instance.buyer.purchased_videos_number += 1
        instance.buyer.save(update_fields=["purchased_videos_number"])

#Update purchase data for each new purchase cancellation
@receiver(pre_delete, sender=Purchase)
def decrease_purchased_videos_number_and_archive_purchase(sender, instance, **kwargs):

    #Decrease user's purchased videos number for each new video purchase
    instance.buyer.purchased_videos_number -= 1
    instance.buyer.save(update_fields=["purchased_videos_number"])

    #Move purchase to CancelledPurchase before deleting from Purchase
    CancelledPurchase.objects.create(
        buyer=instance.buyer,
        video=instance.video,
        time_of_initial_purchase=instance.time_of_purchase,
        fee_currency=instance.fee_currency,
        fee_amount=instance.fee_amount
    )