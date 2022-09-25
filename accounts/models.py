from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.base_user import BaseUserManager

from django.db.models import JSONField

from django.conf import settings

import uuid

class AccountManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """Create and save an Account with the given email and password."""
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class Account (AbstractUser):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    email = models.EmailField("email address", unique=True)

    display_name = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(max_length=300, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    cover_photo = models.ImageField(upload_to="cover_photos/", blank=True, null=True)
    active_subscriptions_number = models.PositiveIntegerField(default=0)
    expired_subscriptions_number = models.PositiveIntegerField(default=0)
    purchased_videos_number = models.PositiveIntegerField(default=0)
    saved_videos_number = models.PositiveIntegerField(default=0)
    btc_wallet_balance = models.FloatField(default=0.00)
    usd_wallet_balance = models.FloatField(default=0.00)
    payment_info = JSONField(null=True)
    notification_settings = JSONField(null=True)
    blocked_accounts_number = models.PositiveIntegerField(default=0)

    is_creator = models.BooleanField(default=False)

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

class CreatorInfo(models.Model):
    creator = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    subscribers_number = models.PositiveIntegerField(default=0)
    subscription_fee = JSONField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    identity = JSONField(null=True, blank=True)

    def __str___(self):
        return f"{self.creator}'s creator info"