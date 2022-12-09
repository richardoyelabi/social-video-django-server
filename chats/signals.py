from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from chats.models import ChatMessage, Inbox
from media.models import Photo, Video
from subscriptions.models import Subscription
from media.exceptions import MediaUseError


#Make sure accounts can not use media items that do not belong to them in a message
@receiver(pre_save, sender=ChatMessage)
def check_media_ownership(sender, instance, **kwargs):

    if instance.media_item:
        if (instance.media_item.uploader != instance.user):
            raise MediaUseError("This account does not have permission to use the media attached to this message.")


#Make sure photo media doesn't get into video messages and vice versa
@receiver(pre_save, sender=ChatMessage)
def check_media_consistency(sender, instance, **kwargs):

    if instance.media_item:
        if not(
            instance.message_type == "photo"
            and
            instance.media_type == ContentType.objects.get_for_model(Photo)
        ) \
        \
        and not(
            (
                instance.message_type=="free_video" or instance.message_type=="paid_video"
            )
            and
            instance.media_type == ContentType.objects.get_for_model(Video)
        ):

            raise MediaUseError("Message type does not match media type. Please, correct the discrepancy.")


#Make sure no premium video has non-zero purchase amount
@receiver(pre_save, sender=ChatMessage)
def assert_premium_status(sender, instance, **kwargs):

    if instance.message_type=="paid_video":
        if instance.purchase_cost_amount<=0:
            instance.message_type = "free_video"
            instance.save(update_fields=["message_type"])


#Update inboxes of concerned users when a message is created
@receiver(post_save, sender=ChatMessage)
def update_inbox(sender, instance, created, **kwargs):
    if created:
        Inbox.objects.set_inbox(user=instance.user, other_user=instance.receiver, msg=instance.message, read=True)
        Inbox.objects.set_inbox(other_user=instance.user, user=instance.receiver, msg=instance.message, read=False)
        return None


#Make sure a user can only initiate chat with an account they're subscribed to
@receiver(pre_save, sender=ChatMessage)
def enforce_chat_initiation_privileges(sender, instance, **kwargs):

    qlookup = (Q(user=instance.user) & Q(receiver=instance.receiver)) | \
        (Q(user=instance.receiver) & Q(receiver=instance.user))

    if not ChatMessage.objects.filter(qlookup).exists():
        if not Subscription.objects.filter(
            subscriber = instance.user,
            subscribed_to = instance.receiver
        ).exists():
            raise ConnectionRefusedError("Chat initiation is not authorized")


#Make sure all created messages are between accounts with a subscription relationship
@receiver(pre_save, sender=ChatMessage)
def enforce_messaging_privileges(sender, instance, **kwargs):

    user = instance.user
    receiver = instance.receiver

    qlookup = (Q(subscribed_to=user) & Q(subscriber=receiver)) \
        | (Q(subscribed_to=receiver) & Q(subscriber=user))
    
    if not Subscription.objects.filter(qlookup).exists():
        raise ConnectionRefusedError("Chat is not authorized")


#Make sure only verified creators can send premium videos
#Change premium videos to free videos with $0 cost
@receiver(pre_save, sender=ChatMessage)
def restrict_paid_videos(sender, instance, **kwargs):
    user = instance.user

    if instance.message_type=="paid_video":
        if not (user.is_creator and user.creatorinfo.is_verified):
            instance.message_type = "free_video"
            instance.purchase_cost_currency = "usd"
            instance.purchase_cost_amount = 0
