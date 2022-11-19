from rest_framework import serializers
from django.contrib.sites.models import Site
from versatileimagefield.serializers import VersatileImageFieldSerializer
from django.contrib.auth import get_user_model

from media.models import Photo, Video

class PhotoSerializer(serializers.ModelSerializer):
    """Serializer for photo uploads"""
    media = VersatileImageFieldSerializer(sizes="photo_upload")
    uploader = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())

    class Meta:
        model = Photo
        fields = ["public_id", "uploader", "media"]
        read_only_fields = ["public_id"]

class CustomVideoThumbnailSerializer(serializers.FileField):
    """Return a dictionary of urls corresponding to video and its thumbnail"""

    read_only = True

    def to_representation(self, value):

        context_request = None
        if self.context:
            context_request = self.context.get("request", None)

            post_id = self.context.get("view").kwargs.get("post_id")
            video_id = value.instance.public_id

            video_rel_url = f"post/{post_id}/video-stream/{video_id}/"

            domain = Site.objects.get_current().domain

        return {
            "video": f"http://{domain}/{video_rel_url}",
            "thumbnail": f"http://{domain}/{value.url_300x300}"
        }

class VideoSerializer(serializers.ModelSerializer):
    """Serializer for video uploads"""
    media = CustomVideoThumbnailSerializer()
    uploader = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())

    class Meta:
        model = Video
        fields = ["public_id", "uploader", "media"]
        read_only_fields = ["public_id"]