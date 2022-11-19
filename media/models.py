from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from django.conf import settings
from .validators import FileMimeValidator
from media.media_paths import photo_uploads_path, video_uploads_path
from posts.models import Post

from versatileimagefield.fields import VersatileImageField
from videothumbs.fields import VideoThumbnailField
import uuid


class Photo(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="photo_uploads", on_delete=models.SET_NULL, null=True)
    upload_time = models.DateTimeField(auto_now=True)
    media = VersatileImageField(upload_to=photo_uploads_path)

    associated_posts = GenericRelation(Post, related_query_name="photo", content_type_field="media_type", object_id_field="media_id")

    def __str__(self):
        return f"{self.uploader}'s photo {self.public_id}"

class Video(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="video_uploads", on_delete=models.SET_NULL, null=True)
    upload_time = models.DateTimeField(auto_now=True)
    media = VideoThumbnailField(upload_to=video_uploads_path, validators=[FileMimeValidator()], sizes=((300,300),))

    associated_posts = GenericRelation(Post, related_query_name="video", content_type_field="media_type", object_id_field="media_id")

    def __str__(self):
        return f"{self.uploader}'s video {self.public_id}"
