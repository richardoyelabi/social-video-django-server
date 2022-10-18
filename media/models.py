from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from django.conf import settings
from media.media_paths import photo_uploads_path, video_uploads_path
from posts.models import Post

from versatileimagefield.fields import VersatileImageField
from django.core.validators import FileExtensionValidator
import uuid

from transactions.models import Transaction

class Photo(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="photo_uploads", on_delete=models.SET_NULL, null=True)
    content_type = models.CharField(max_length=4, choices=[
        ("post","Feed post"),
        ("chat","Private message")
    ])
    upload_time = models.DateTimeField(auto_now=True)
    image = VersatileImageField(upload_to=photo_uploads_path)

    associated_posts = GenericRelation(Post, related_query_name="photo", content_type_field="media_type", object_id_field="media_id")

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
    video = models.FileField(upload_to=video_uploads_path, validators=[FileExtensionValidator(["mp4"])])
    purchase_cost_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd", blank=True)
    purchase_cost_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00, blank=True)

    associated_posts = GenericRelation(Post, related_query_name="video", content_type_field="media_type", object_id_field="media_id")

    def __str__(self):
        return f"{self.uploader}'s video {self.public_id}"
