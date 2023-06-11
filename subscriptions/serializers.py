from django.contrib.auth import get_user_model

from rest_framework import serializers
from subscriptions.models import Subscription
from accounts.models import CreatorInfo


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for SubscriptionView"""

    class Meta:
        model = Subscription
        fields = []


class SetSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer to set subscription fee of creators"""

    creator = serializers.SlugRelatedField(
        slug_field="public_id", queryset=get_user_model().objects.all()
    )

    class Meta:
        model = CreatorInfo
        fields = ["creator", "subscription_fee_currency", "subscription_fee_amount"]
