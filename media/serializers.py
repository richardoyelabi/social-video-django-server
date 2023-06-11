from rest_framework import serializers
from django.contrib.sites.models import Site
from versatileimagefield.serializers import VersatileImageFieldSerializer
from django.contrib.auth import get_user_model

from media.models import Photo, Video
from media.validators import FileMimeValidator


# Custom VersatileImageField serializer to build absolute uri
# when the default way of using request.build_absolute_uri won't work
class CustomImageFieldSerializer(VersatileImageFieldSerializer):
    """Override VersatileImageField's default way of building absolute uri"""

    # Use Site to build absolute uri if request object is not available
    def to_native(self, value):
        """For djangorestframework <=2.3.14.
        to_representation returns to_native"""

        default = super().to_native(value)
        if not "request" in self.context.keys():
            domain = Site.objects.get_current().domain
            for k, v in default.items():
                default[k] = f"http://{domain}{v}"
        return default


class PhotoSerializer(serializers.ModelSerializer):
    """Serializer for photo uploads"""

    media = CustomImageFieldSerializer(sizes="photo_upload")
    uploader = serializers.SlugRelatedField(
        slug_field="public_id", queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Photo
        fields = ["public_id", "uploader", "media"]
        read_only_fields = ["public_id"]


class CustomVideoThumbnailSerializer(serializers.FileField):
    """Return a dictionary of urls corresponding to video and its thumbnail (and preview)"""

    read_only = True

    def to_representation(self, value):
        # If video is viewed as an element of a post
        if self.root.instance._meta.model.__name__ == "Post":
            post_id = self.root.instance.public_id
            video_id = value.instance.public_id

            video_rel_url = f"post/{post_id}/video-stream/{video_id}/"

        # If video is viewed as an element of a message
        elif self.root.instance._meta.model.__name__ == "ChatMessage":
            message_id = self.root.instance.public_id
            video_id = value.instance.public_id

            video_rel_url = f"chat/message/{message_id}/video-stream/{video_id}/"

        domain = Site.objects.get_current().domain

        ret = {
            "video": f"http://{domain}/{video_rel_url}",
            "thumbnail": f"http://{domain}{value.url_300x300}/",
        }

        # If video is viewed as an element of a post and the post is premium
        if self.root.instance._meta.model.__name__ == "Post":
            if self.root.instance.post_type == "paid_video":
                if self.root.instance.video_preview:
                    preview = self.root.instance.video_preview
                    ret[
                        "video_preview"
                    ] = f"http://{domain}/post/{post_id}/video-preview/{video_id}/"

        return ret


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for video uploads"""

    media = CustomVideoThumbnailSerializer()
    uploader = serializers.SlugRelatedField(
        slug_field="public_id", queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Video
        fields = ["public_id", "uploader", "media"]
        read_only_fields = ["public_id"]

    def validate_media(self, value):
        validator = FileMimeValidator()
        validator(value, api_call=True)
        return value
