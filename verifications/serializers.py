from rest_framework import serializers

from .models import IdUpload

class IdUploadSerializer(serializers.ModelSerializer):
    """Serializer for IdUploadView"""

    class Meta:
        model = IdUpload
        fields = ["public_id", "creator", "type", "upload_time", "upload"]
        read_only_fields = ["public_id", "upload_time"]