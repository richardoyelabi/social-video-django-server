from rest_framework import serializers
from django.contrib.auth import get_user_model
from versatileimagefield.serializers import VersatileImageFieldSerializer
from dj_rest_auth.serializers import UserDetailsSerializer

from media.models import Photo, Video
from .models import Inbox, ChatMessage
from media.serializers import PhotoSerializer, VideoSerializer


class AccountChatSerializer(UserDetailsSerializer):
    """Serializer for users on chat views and consumers"""

    public_id = serializers.UUIDField(read_only=False)

    profile_photo = VersatileImageFieldSerializer(sizes="profile_photo", allow_null=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "public_id", "display_name", "profile_photo", "online", "last_online"]
        read_only_fields = ["username", "display_name", "profile_photo"]


class InboxSerializer(serializers.ModelSerializer):
    """Serializer to retrieve user's inbox"""

    user = AccountChatSerializer(many=False, read_only=True)
    second = serializers.SerializerMethodField()
    request = serializers.SerializerMethodField()
    last_message_from = AccountChatSerializer(many=False, read_only=True)

    def get_second(self, obj):
        if 'request' in self.context:
            profile_serializer = AccountChatSerializer(instance=get_user_model().objects.get(id=obj.second.id),
                                                           context={'request': self.context['request']})
            return profile_serializer.data
        else:
            profile_serializer = AccountChatSerializer(instance=get_user_model().objects.get(id=obj.second.id))
            return profile_serializer.data

    def get_request(self, obj):
        if 'request' in self.context:
            return True
        else:
            return False

    class Meta:
        model = Inbox
        fields = ['public_id', 'user', 'second', 'last_message', 'timestamp', 'updated', 'request', 'read', 'last_message_from']


class TextMessageDetailSerializer(serializers.ModelSerializer):
    """Serializer to retrieve text messages"""

    user = AccountChatSerializer(many=False, read_only=True)
    receiver = AccountChatSerializer(many=False, read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['public_id', 'user', 'receiver', 'message', 'timestamp', "message_type", "is_special_request", "is_tip_message", "tip_currency", "tip_amount"]
        read_only_fields = ["public_id", "timestamp", "status"]


class BaseMediaMessageDetailSerializer(TextMessageDetailSerializer):
    """Base serializer to retrieve messages with media attachment"""

    media_item = serializers.FileField()

    class Meta:
        model = ChatMessage
        fields = ["public_id", "user", "receiver", "message", "timestamp", "message_type", "media_item", "is_special_request"]
        read_only_fields = ["public_id", "timestamp", "status"]


class PhotoMessageDetailSerializer(BaseMediaMessageDetailSerializer):
    """Serializer to retrieve photo messages"""

    media_item = PhotoSerializer(read_only=True)


class VideoMessageDetailSerializer(BaseMediaMessageDetailSerializer):
    """Serializer to retrieve video messages"""

    media_item = VideoSerializer(read_only=True)


class PaidVideoMessageDetailSerializer(VideoMessageDetailSerializer):
    """Serializer for paid video messages"""

    class Meta:
        model = ChatMessage
        fields = ["public_id", "user", "receiver", "message", "timestamp", "message_type", "media_item", "purchase_cost_currency", "purchase_cost_amount"]
        read_only_fields = ["public_id", "timestamp", "status"]


class MessageListSerializer(serializers.ModelSerializer):
    """Serializer for listing messages in a chat"""

    message_details = serializers.SerializerMethodField()

    def get_message_details(self, instance):
        message_type = instance.message_type
        if message_type=="text":
            serializer = TextMessageDetailSerializer
        elif message_type=="photo":
            serializer = PhotoMessageDetailSerializer
        elif message_type==("free_video"):
            serializer = VideoMessageDetailSerializer
        elif message_type==("paid_video"):
            serializer = PaidVideoMessageDetailSerializer

        return serializer(instance).data

    class Meta:
        model = ChatMessage
        fields = ["message_details"]


class TextMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer to create text messages"""

    user = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())
    receiver = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())

    class Meta:
        model = ChatMessage
        fields = ['thread', 'user', 'receiver', 'message', "message_type", "is_special_request", "is_tip_message", "tip_currency", "tip_amount"]


class PhotoMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer to create photo messages"""

    user = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())
    receiver = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())

    media_item = serializers.SlugRelatedField(slug_field="public_id", queryset=Photo.objects.all())

    class Meta:
        model = ChatMessage
        fields = ["thread", "user", "receiver", "message", "message_type", "media_item", "is_special_request"]


class VideoMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer to create video messages"""

    user = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())
    receiver = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())

    media_item = serializers.SlugRelatedField(slug_field="public_id", queryset=Video.objects.all())

    class Meta:
        model = ChatMessage
        fields = ["thread", "user", "receiver", "message", "message_type", "media_item", "is_special_request"]


class PaidVideoMessageCreateSerializer(VideoMessageCreateSerializer):
    """Serializer to create paid video messages"""

    class Meta:
        model = ChatMessage
        fields = ["thread", "user", "receiver", "message", "message_type", "media_item", "purchase_cost_currency", "purchase_cost_amount"]
