from rest_framework import serializers
from video_saves.models import VideoSave


class VideoSaveSerializer(serializers.ModelSerializer):
    """Serializer for VideoSaveView"""

    class Meta:
        model = VideoSave
        fields = []
