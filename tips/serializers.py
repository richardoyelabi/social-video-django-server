from rest_framework import serializers
from tips.models import Tip


class TipSerializer(serializers.ModelSerializer):
    """Serializer for TipView"""

    class Meta:
        model = Tip
        fields = ["sender", "receiver", "created", "fee_currency", "fee_amount"]
        read_only_fields = ["created"]
