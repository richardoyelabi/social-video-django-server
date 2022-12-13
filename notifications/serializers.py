from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):

    public_id = serializers.UUIDField()
    timestamp = serializers.DateTimeField()
    message = serializers.CharField()
    extra = serializers.CharField()
    icon = serializers.URLField()