from django.db import models
from rest_framework import serializers
from django.contrib.sites.models import Site
from media.serializers import CustomImageFieldSerializer

from media.models import Photo, Video, Media


class VaultPhotoSerializer(serializers.ModelSerializer):
    """Serializer for photos in ChatVaultView"""

    media = CustomImageFieldSerializer(sizes="photo_upload")

    class Meta:
        model = Photo
        fields = ["public_id", "upload_time", "media"]


class VaultVideoThumbnailSerializer(serializers.FileField):
    """Return a dictionary of urls corresponding to video and its thumbnail"""

    read_only = True

    def to_representation(self, value):
        video_id = value.instance.public_id
        video_rel_url = f"chat/vault/video-stream/{video_id}/"
        domain = Site.objects.get_current().domain

        ret = {
            "video": f"http://{domain}/{video_rel_url}",
            "thumbnail": f"http://{domain}/{value.url_300x300}/",
        }
        return ret


class VaultVideoSerializer(serializers.ModelSerializer):
    """Serializer for videos in ChatVaultView"""

    media = VaultVideoThumbnailSerializer()

    class Meta:
        model = Video
        fields = ["public_id", "upload_time", "media"]


class VaultListSerializer(serializers.ListSerializer):
    """Custom ListSerializer to implement custom to_representation for each media item in vault"""

    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data

        to_rep = []
        for item in iterable:
            to_rep += [self.get_to_rep(item)]
        return to_rep

    def get_to_rep(self, instance):
        model = instance._meta.model

        if model == Media:
            instance = instance.media_item
            model = instance._meta.model

        self.child.Meta.model = model
        instance.type = model.__name__.lower()

        def get_serializer():
            if model == Photo:
                return VaultPhotoSerializer
            else:
                return VaultVideoSerializer

        serializer = get_serializer()

        ret = serializer(instance).to_representation(instance)

        ret["type"] = instance.type

        return ret


class VaultSerializer(serializers.ModelSerializer):
    """Common serializer for all media items in vault"""

    class Meta:
        list_serializer_class = VaultListSerializer
        model = None
        fields = "__all__"
