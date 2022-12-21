from rest_framework import serializers

from django.contrib.auth import get_user_model


class NotificationSerializer(serializers.Serializer):

    public_id = serializers.UUIDField()
    timestamp = serializers.DateTimeField()
    message = serializers.CharField()
    extra = serializers.CharField()
    icon = serializers.URLField()


class NotificationSettingsListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ["email_message", "email_promotion", "site_message", "site_promotion"]