from rest_framework import serializers
from special_requests.models import MessagePurchase


class MessagePurchaseSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseView"""

    class Meta:
        model = MessagePurchase
        fields = []
