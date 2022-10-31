from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from django.conf import settings
from .account_manager import AccountManager
from media.media_paths import profile_photos_path, cover_photos_path
from subscriptions.models import Subscription
from transactions.models import Transaction
from media.models import Video
from video_purchases.models import Purchase
from posts.models import Post, Like, Comment
from video_saves.models import VideoSave

from versatileimagefield.fields import VersatileImageField
from django.db.models import JSONField
import uuid

class Account(AbstractUser):

    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField("email address", unique=True)

    display_name = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(max_length=300, blank=True, null=True)

    profile_photo = VersatileImageField(upload_to=profile_photos_path, blank=True, null=True)
    cover_photo = VersatileImageField(upload_to=cover_photos_path, blank=True, null=True)
    
    active_subscriptions_number = models.PositiveIntegerField(default=0)
    expired_subscriptions_number = models.PositiveIntegerField(default=0)
    
    purchased_videos_number = models.PositiveIntegerField(default=0)
    
    saved_videos_number = models.PositiveIntegerField(default=0)
    
    btc_wallet_balance = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)
    usd_wallet_balance = models.DecimalField(max_digits=20, decimal_places=10, default=0.00)
    
    payment_info = JSONField(null=True)
    
    notification_settings = JSONField(null=True, blank=True)
    
    blocked_accounts_number = models.PositiveIntegerField(default=0)
    
    is_creator = models.BooleanField(default=False)

    subscriptions = models.ManyToManyField("self", through=Subscription, related_name="subscribers", symmetrical=False)
    purchased_videos = models.ManyToManyField(Video, through=Purchase, related_name="buyers")

    saved_videos = models.ManyToManyField(Post, through=VideoSave, related_name="saves")

    post_likes = models.ManyToManyField(Post, through=Like, related_name="liked_by")
    post_comments = models.ManyToManyField(Post, through=Comment, related_name="commented_on_by")

    def save(self, *args, **kwargs):

        #Set display_name to username by default
        if not self.display_name:
            self.display_name = self.username

        super().save(*args, **kwargs)


    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = AccountManager()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("profile", kwargs={"public_id": self.public_id}) 

class CreatorInfo(models.Model):
    creator = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name="creatorinfo")
    subscribers_number = models.PositiveIntegerField(default=0)
    subscription_fee_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd", blank=True)
    subscription_fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00, blank=True)
    is_verified = models.BooleanField(default=False)
    identity = JSONField(null=True, blank=True)

    def __str__(self):
        return f"Creator {self.creator.username}"
