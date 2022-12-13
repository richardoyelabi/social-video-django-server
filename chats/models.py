from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from model_utils import FieldTracker

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from transactions.models import Transaction

import uuid

channel_layer = get_channel_layer()

User = get_user_model()


# Thread Manager -> Manages thread object operations
class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_id):
        # get_or_create -> Finds existing thread or creates new one
        user_id = user.public_id
        if user_id == other_id:
            return None
        qlookup1 = Q(first__public_id=user_id) & Q(second__public_id=other_id)
        qlookup2 = Q(first__public_id=other_id) & Q(second__public_id=user_id)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            try:
                user2 = User.objects.get(public_id=other_id)
            except User.DoesNotExist:
                return None, False
            if user != user2:
                obj = self.model(
                    first=user,
                    second=user2
                )
                obj.save()
                return obj, True
            return None, False


# Each thread consist of 2 users
class Thread(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_first')
    second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    class Meta:
        unique_together = ['first', 'second']

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def __str__(self):
        return f"{self.first} - {self.second} Thread - ID: ${self.pk}"


class InboxManager(models.Manager):
    def set_inbox(self, user, other_user, msg, read=False):
        inbox_object, created_1 = self.get_or_create(user=user, second=other_user)
        inbox_object.last_message = msg
        inbox_object.read = read
        inbox_object.last_message_from = user
        inbox_object.save()
        from .serializers import InboxSerializer
        ib1 = InboxSerializer(instance=inbox_object).data
        async_to_sync(channel_layer.group_send)(f"inbox_{inbox_object.user.username}",
                                                {"type": "update_inbox",
                                                 "content": {
                                                     'type': 'inbox_update',
                                                     'data': ib1
                                                 }})

        return None

    def read_inbox(self, user, other_user):
        inbox = self.get_queryset().filter(user=user, second=other_user)
        if inbox.count() == 1:
            inbox_obj = inbox.first()
            inbox_obj.read = True
            inbox_obj.save()
            from .serializers import InboxSerializer
            inbox_data = InboxSerializer(instance=inbox_obj).data
            async_to_sync(channel_layer.group_send)(f"inbox_{inbox_obj.user.username}",
                                                    {"type": "update_inbox",
                                                     "content": {
                                                         'type': 'read_update',
                                                         'data': inbox_data
                                                     }})

            return None


class Inbox(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_user')
    second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_second_user')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_message = models.TextField(max_length=2048, blank=True, default="")
    last_message_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='last_message_user',blank=True, null=True)
    read = models.BooleanField(default=False)

    tracker = FieldTracker()
    objects = InboxManager()

    class Meta:
        unique_together = ['user', 'second']
        verbose_name = 'User Inbox'
        verbose_name_plural = 'User Inbox'

    def __str__(self):
        return f"{self.user} - {self.second} Inbox - ID: {self.pk}"


class ChatMessage(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, verbose_name='sender', related_name='message_sender',
                             on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='message_receiver', verbose_name='receiver',
                                 on_delete=models.CASCADE)
    inbox = models.ManyToManyField(to=Inbox, blank=True)
    message = models.TextField(max_length=2048, blank=True, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    message_type = models.CharField(max_length=12, null=False, blank=False, choices=[
        ("text", "Text"),
        ("photo", "Photo"),
        ("free_video", "Free video"),
        ("paid_video", "Premium video"),
    ])

    media_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={"model__in":(
        "photo",
        "video"
    )})
    media_id = models.PositiveIntegerField(null=True, blank=True)
    media_item = GenericForeignKey("media_type", "media_id")

    purchase_cost_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd", blank=True)
    purchase_cost_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00, blank=True)

    is_special_request = models.BooleanField(default=False)

    is_tip_message = models.BooleanField(default=False)
    tip_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd", blank=True)
    tip_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["media_type", "media_id"]),
        ]
