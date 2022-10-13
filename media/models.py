from django.db import models
from django.conf import settings

from versatileimagefield.fields import VersatileImageField
from django.core.validators import FileExtensionValidator

import uuid

class Photo(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="photo_uploads", on_delete=models.SET_NULL, null=True)
    content_type = models.CharField(max_length=4, choices=[
        ("post","Feed post"),
        ("chat","Private message")
    ])
    upload_time = models.DateTimeField(auto_now=True)
    image = VersatileImageField(upload_to="photos/%Y/%m/%d")

    def __str__(self):
        return f"{self.uploader}'s photo {self.public_id}"

class Video(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="video_uploads", on_delete=models.SET_NULL, null=True)
    content_type = models.CharField(max_length=10, choices=[
        ("paid_post", "Premium post"),
        ("paid_chat", "Premium message"),
        ("free_post","Free post"),
        ("free_chat", "Free Message")
    ])
    upload_time = models.DateTimeField(auto_now=True)
    video = models.FileField(upload_to="videos/%Y/%m/%d", validators=[FileExtensionValidator(["mp4"])])

    def __str__(self):
        return f"{self.uploader}'s video {self.public_id}"