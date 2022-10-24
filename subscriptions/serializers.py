from rest_framework import serializers
from subscriptions.models import Subscription
from django.conf import settings
from django.contrib.auth import get_user_model

class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for SubscriptionView"""
    class Meta:
        model = Subscription
        fields = []
