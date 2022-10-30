from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from django.contrib.auth import get_user_model

from media.models import Photo, Video

class PhotoSerializer(serializers.ModelSerializer):
    """Serializer for photo uploads"""
    media = VersatileImageFieldSerializer(sizes="photo_upload")
    uploader = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())

    class Meta:
        model = Photo
        fields = ["public_id", "uploader", "content_type", "media"]
        read_only_fields = ["public_id"]

class VideoSerializer(serializers.ModelSerializer):
    """Serializer for video uploads"""
    media = serializers.FileField
    uploader = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())

    class Meta:
        model = Video
        fields = ["public_id", "uploader", "content_type", "media"]
        read_only_fields = ["public_id"]