from rest_framework import serializers
from video_purchases.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseView"""

    class Meta:
        model = Purchase
        fields = []
