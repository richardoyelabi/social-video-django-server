from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

from transactions.models import Transaction

import uuid

class Post(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.SET_NULL, null=True)
    post_type = models.CharField(max_length=12, null=False, blank=False, choices=[
        ("photo", "Photo"),
        ("free_video", "Free video"),
        ("paid_video", "Premium video"),
    ])
    upload_time = models.DateTimeField(auto_now=True)
    caption = models.TextField(max_length=1024, blank=True, default="")

    media_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, limit_choices_to={"model__in":(
        "photo",
        "video"
    )})
    media_id = models.PositiveIntegerField()
    media_item = GenericForeignKey("media_type", "media_id")

    likes_number = models.PositiveIntegerField(default=0)
    comments_number = models.PositiveIntegerField(default=0)

    purchase_cost_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd", blank=True)
    purchase_cost_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["media_type", "media_id"]),
        ]

    def __str__(self):
        return f"{self.uploader}'s post {self.public_id}"

class Like(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account} likes {self.post}"

class Comment(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=256)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account}'s comment on {self.post}"
