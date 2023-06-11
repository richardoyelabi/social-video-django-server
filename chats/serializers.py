from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import models
from dj_rest_auth.serializers import UserDetailsSerializer

from media.models import Photo, Video
from .models import Inbox, ChatMessage
from media.serializers import (
    PhotoSerializer,
    VideoSerializer,
    CustomImageFieldSerializer,
)
from transactions.currency_convert import convert_currency


class AccountChatSerializer(UserDetailsSerializer):
    """Serializer for users on chat views and consumers"""

    public_id = serializers.UUIDField(read_only=False)

    profile_photo = CustomImageFieldSerializer(
        sizes="profile_photo", allow_null=True, read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "public_id", "display_name", "profile_photo"]
        read_only_fields = ["username", "display_name", "profile_photo"]


class InboxSerializer(serializers.ModelSerializer):
    """Serializer to retrieve user's inbox"""

    second = serializers.SerializerMethodField()
    last_message_from = serializers.SlugRelatedField(
        slug_field="public_id", queryset=get_user_model().objects.all()
    )

    def get_second(self, obj):
        if "request" in self.context:
            profile_serializer = AccountChatSerializer(
                instance=get_user_model().objects.get(id=obj.second.id),
                context={"request": self.context["request"]},
            )
            return profile_serializer.data
        else:
            profile_serializer = AccountChatSerializer(
                instance=get_user_model().objects.get(id=obj.second.id)
            )
            return profile_serializer.data

    class Meta:
        model = Inbox
        fields = [
            "public_id",
            "second",
            "last_message",
            "timestamp",
            "updated",
            "read",
            "last_message_from",
        ]


class TextMessageDetailSerializer(serializers.ModelSerializer):
    """Serializer to retrieve text messages"""

    user = serializers.SlugRelatedField(
        slug_field="public_id", queryset=get_user_model().objects.all()
    )
    receiver = serializers.SlugRelatedField(
        slug_field="public_id", queryset=get_user_model().objects.all()
    )

    class Meta:
        model = ChatMessage
        fields = [
            "public_id",
            "user",
            "receiver",
            "message",
            "timestamp",
            "message_type",
            "is_special_request",
            "is_tip_message",
            "tip_currency",
            "tip_amount",
        ]
        read_only_fields = ["public_id", "timestamp", "status"]


class BaseMediaMessageDetailSerializer(TextMessageDetailSerializer):
    """Base serializer to retrieve messages with media attachment"""

    media_item = serializers.FileField()

    class Meta:
        model = ChatMessage
        fields = [
            "public_id",
            "user",
            "receiver",
            "message",
            "timestamp",
            "message_type",
            "media_item",
            "is_special_request",
        ]
        read_only_fields = ["public_id", "timestamp", "status"]


class PhotoMessageDetailSerializer(BaseMediaMessageDetailSerializer):
    """Serializer to retrieve photo messages"""

    media_item = PhotoSerializer(read_only=True)


class VideoMessageDetailSerializer(BaseMediaMessageDetailSerializer):
    """Serializer to retrieve video messages"""

    media_item = VideoSerializer(read_only=True)


class PaidVideoMessageDetailSerializer(VideoMessageDetailSerializer):
    """Serializer for paid video messages"""

    usd_purchase_cost = serializers.SerializerMethodField()
    btc_purchase_cost = serializers.SerializerMethodField()

    def get_usd_purchase_cost(self, obj):
        return str(
            convert_currency(
                obj.purchase_cost_currency, "usd", obj.purchase_cost_amount
            )
        )

    def get_btc_purchase_cost(self, obj):
        return str(
            convert_currency(
                obj.purchase_cost_currency, "btc", obj.purchase_cost_amount
            )
        )

    class Meta:
        model = ChatMessage
        fields = [
            "public_id",
            "user",
            "receiver",
            "message",
            "timestamp",
            "message_type",
            "media_item",
            "usd_purchase_cost",
            "btc_purchase_cost",
        ]
        read_only_fields = ["public_id", "timestamp", "status"]


class MessageListSerializer(serializers.ListSerializer):
    """Custom serializer to implement custom to_representation for each message in list"""

    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data

        to_rep = []
        for item in iterable:
            to_rep += [self.get_to_rep(item)]
        return to_rep

    def get_to_rep(self, instance):
        if instance.message_type == "text":
            return TextMessageDetailSerializer(instance).to_representation(instance)

        elif instance.message_type == "photo":
            return PhotoMessageDetailSerializer(instance).to_representation(instance)

        elif instance.message_type == "free_video":
            return VideoMessageDetailSerializer(instance).to_representation(instance)

        elif instance.message_type == "paid_video":
            return PaidVideoMessageDetailSerializer(instance).to_representation(
                instance
            )


class MessageDetailSerializer(serializers.ModelSerializer):
    """Common serializer for all messages in message list"""

    class Meta:
        list_serializer_class = MessageListSerializer
        model = ChatMessage
        fields = "__all__"


class TextMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer to create text messages"""

    user = serializers.SlugRelatedField(
        slug_field="public_id", queryset=get_user_model().objects.all()
    )
    receiver = serializers.SlugRelatedField(
        slug_field="public_id", queryset=get_user_model().objects.all()
    )

    class Meta:
        model = ChatMessage
        fields = [
            "thread",
            "user",
            "receiver",
            "message",
            "message_type",
            "is_special_request",
            "is_tip_message",
            "tip_currency",
            "tip_amount",
        ]


class PhotoMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer to create photo messages"""

    user = serializers.SlugRelatedField(
        slug_field="public_id", queryset=get_user_model().objects.all()
    )
    receiver = serializers.SlugRelatedField(
        slug_field="public_id", queryset=get_user_model().objects.all()
    )

    media_item = serializers.SlugRelatedField(
        slug_field="public_id", queryset=Photo.objects.all()
    )

    class Meta:
        model = ChatMessage
        fields = [
            "thread",
            "user",
            "receiver",
            "message",
            "message_type",
            "media_item",
            "is_special_request",
        ]


class VideoMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer to create video messages"""

    user = serializers.SlugRelatedField(
        slug_field="public_id", queryset=get_user_model().objects.all()
    )
    receiver = serializers.SlugRelatedField(
        slug_field="public_id", queryset=get_user_model().objects.all()
    )

    media_item = serializers.SlugRelatedField(
        slug_field="public_id", queryset=Video.objects.all()
    )

    class Meta:
        model = ChatMessage
        fields = [
            "thread",
            "user",
            "receiver",
            "message",
            "message_type",
            "media_item",
            "is_special_request",
        ]


class PaidVideoMessageCreateSerializer(VideoMessageCreateSerializer):
    """Serializer to create paid video messages"""

    class Meta:
        model = ChatMessage
        fields = [
            "thread",
            "user",
            "receiver",
            "message",
            "message_type",
            "media_item",
            "purchase_cost_currency",
            "purchase_cost_amount",
        ]
