from rest_framework import serializers
from subscriptions.models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for SubscriptionView"""
    class Meta:
        model = Subscription
        fields = []
