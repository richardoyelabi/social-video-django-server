from rest_framework import serializers
from django.http import HttpRequest
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

class CustomVideoThumbnailSerializer(serializers.FileField):
    """Return a dictionary of urls corresponding to video and its thumbnail"""

    read_only = True

    def to_representation(self, value):
        context_request = None
        if self.context:
            context_request = self.context.get("request", None)
        return {
            "thumbnail": HttpRequest.build_absolute_uri(value.get_thumbnail_url((300,300))),
            "video": HttpRequest.build_absolute_uri(value.path),
        }

class VideoSerializer(serializers.ModelSerializer):
    """Serializer for video uploads"""
    media = CustomVideoThumbnailSerializer()
    uploader = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())

    class Meta:
        model = Video
        fields = ["public_id", "uploader", "content_type", "media"]
        read_only_fields = ["public_id"]