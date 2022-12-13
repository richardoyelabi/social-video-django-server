from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.sites.models import Site
from rest_framework.renderers import JSONRenderer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.mail import send_mail

from django.conf import settings
from posts.models import Like, Comment
from subscriptions.models import Subscription
from video_purchases.models import Purchase
from chats.models import ChatMessage
from special_requests.models import SpecialRequest, MessagePurchase
from tips.models import Tip
from notifications.serializers import NotificationSerializer

import uuid


class Notification (models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE)

    record_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    record_id = models.PositiveIntegerField()
    record = GenericForeignKey("record_type", "record_id")

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["record_type", "record_id"]),
        ]

    @classmethod
    def format(self, record):
        """Format notification instance into comprehensible message meant for receiver"""

        def get_icon_url (photo):
            """Build icon url from icon photo"""

            icon_size = "100x100"

            if photo:
                rel_url = photo.thumbnail[icon_size]

                domain = Site.objects.get_current().domain

                url = f"http://{domain}{rel_url}"
                
                return url


        model = record._meta.model if record else None

        message, extra, icon = "", "", ""

        if model==Like:
            
            message = f"{record.account.display_name} liked your post"

            extra = f"{record.post.caption}"

            icon = get_icon_url(record.account.profile_photo)

        elif model==Comment:

            message = f"{record.account.display_name} commented on your post {record.post.caption}"

            extra = f"{record.comment_text}"

            icon = get_icon_url(record.account.profile_photo)

        elif model==Subscription:

            message = f"{record.subscriber.display_name} subscribed to your content"

            icon = get_icon_url(record.subscriber.profile_photo)

        elif model==Purchase:

            message = f"{record.buyer.display_name} purchased your video"

            extra = f"{record.video_post.caption}"

            icon = get_icon_url(record.buyer.profile_photo)

        elif model==ChatMessage:

            message = f"{record.user.display_name} sent you a direct message"

            extra = f"{record.message} + media attachment" if record.media_item \
                else f"{record.message}"

            icon = get_icon_url(record.user.profile_photo)

        elif model==SpecialRequest:
            
            message = f"{record.request_by.display_name} sent a special request"

            extra = f"{record.request.message} + media attachment" if record.request.media_item \
                else f"{record.request.message}"

            icon = get_icon_url(record.request_by.profile_photo)

        elif model==MessagePurchase:

            message = f"{record.buyer.display_name} unlocked your message"

            extra = f"{record.video_message.message}"

            icon = get_icon_url(record.buyer.profile_photo)

        elif model==Tip:

            message = f"{record.sender.display_name} sent you a tip"

            extra = f"{record.tip_message.message}"

            icon = get_icon_url(record.sender.profile_photo)

        return dict(message=message, icon=icon, extra=extra)

    @classmethod
    def notify(self, receiver, record):
        """Send notification to concerned user"""

        def email_notify(receiver, record):
            """Send notification to user via email"""
            
            payload = self.format(record)

            subject = payload.get("message")

            message = f"Hey {receiver.username}. \n\
                {payload.get('message')} \n\
                    {payload.get('extra')}"

            email_from = "admin@email.com"
            recipient_list = [receiver.email]

            send_mail( subject, message, email_from, recipient_list )

        def site_notify(receiver, record):
            """Send notification to user via site notification"""

            notification = Notification(receiver = receiver, record = record)
            notification.save()

            receiver.notification_seen = False
            receiver.save(update_fields=["notification_seen"])

            if receiver.connected:

                data = self.format(record)

                data["public_id"] = notification.public_id
                data["timestamp"] = notification.timestamp

                serializer = NotificationSerializer(data)

                data = serializer.data
                
                async_to_sync(get_channel_layer().group_send)(
                    f"notification_{receiver.public_id}",
                    {
                        "type": "site_notification",
                        "content": {
                            "type": "site_notification",
                            "data": data
                        }
                    }
                )

            else:
                email_notify(receiver, record)
        
        if receiver.site_message:
            site_notify(receiver, record)

        elif receiver.email_message:
            email_notify(receiver, record)