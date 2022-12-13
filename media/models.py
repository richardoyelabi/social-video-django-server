from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save

from django.conf import settings
from .validators import FileMimeValidator
from media.media_paths import photo_uploads_path, video_uploads_path
from posts.models import Post
from chats.models import ChatMessage

from versatileimagefield.fields import VersatileImageField
from videothumbs.fields import VideoThumbnailField
import uuid


class Photo(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="photo_uploads", on_delete=models.SET_NULL, null=True)
    upload_time = models.DateTimeField(auto_now=True)
    media = VersatileImageField(upload_to=photo_uploads_path)

    associated_posts = GenericRelation(Post, related_query_name="photo", content_type_field="media_type", object_id_field="media_id", null=True, blank=True)
    associated_chat_messages = GenericRelation(ChatMessage, related_query_name="photo", content_type_field="media_type", object_id_field="media_id", null=True, blank=True)

    def __str__(self):
        return f"{self.uploader}'s photo {self.public_id}"


class Video(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="video_uploads", on_delete=models.SET_NULL, null=True)
    upload_time = models.DateTimeField(auto_now=True)
    media = VideoThumbnailField(upload_to=video_uploads_path, validators=[FileMimeValidator()], sizes=((300,300),))

    associated_posts = GenericRelation(Post, related_query_name="video", content_type_field="media_type", object_id_field="media_id", null=True, blank=True)
    associated_chat_messages = GenericRelation(ChatMessage, related_query_name="video", content_type_field="media_type", object_id_field="media_id", null=True, blank=True)


    def __str__(self):
        return f"{self.uploader}'s video {self.public_id}"


class Media(models.Model):
    public_id = models.UUIDField()
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="media_uploads", on_delete=models.SET_NULL, null=True)
    upload_time = models.DateTimeField()

    media_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={"model__in":(
        "photo",
        "video"
    )})
    media_id = models.PositiveIntegerField(null=True, blank=True)
    media_item = GenericForeignKey("media_type", "media_id")

    class Meta:
        indexes = [
            models.Index(fields=["media_type", "media_id"]),
        ]


def create_media(sender, instance, created, **kwargs):
    """
    Post save handler to create/update Media instances when
    Photo or Video is created/updated
    """
    media_type = ContentType.objects.get_for_model(instance)
    try:
        media= Media.objects.get(media_type=media_type,
                             media_id=instance.id)
    except Media.DoesNotExist:
        media = Media(media_type=media_type, media_id=instance.id)
    media.public_id = instance.public_id
    media.uploader = instance.uploader
    media.upload_time = instance.upload_time
    media.save()


post_save.connect(create_media, sender=Photo)
post_save.connect(create_media, sender=Video)
