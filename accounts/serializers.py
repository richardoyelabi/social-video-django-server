from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from accounts.models import CreatorInfo
from media.serializers import CustomImageFieldSerializer
from transactions.currency_convert import convert_currency


class CustomRegisterSerializer(RegisterSerializer):
    """Custom serializer for signup page"""

    is_creator = serializers.BooleanField()

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'is_creator': self.validated_data.get('is_creator')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
            )
        user.is_creator = self.cleaned_data.get("is_creator")
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class UserPublicProfileSerializer(UserDetailsSerializer):
    """Serializer for non-creator user's profile view as seen by other users"""

    public_id = serializers.UUIDField(read_only=False)

    profile_photo = CustomImageFieldSerializer(sizes="profile_photo", allow_null=True, read_only=True)
    cover_photo = CustomImageFieldSerializer(sizes="cover_photo", allow_null=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "public_id", "display_name", "bio", "profile_photo", "cover_photo"]
        read_only_fields = ["username", "display_name", "bio", "profile_photo", "cover_photo"]


class UserPrivateProfileSerializer(UserDetailsSerializer):
    """Serializer for non-creator user's profile view as seen by the user"""

    profile_photo = CustomImageFieldSerializer(sizes="profile_photo", allow_null=True)
    cover_photo = CustomImageFieldSerializer(sizes="cover_photo", allow_null=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "public_id", "display_name", "bio", "is_creator", "profile_photo", "cover_photo", "btc_wallet_balance", "usd_wallet_balance"]
        read_only_fields = ["public_id", "is_creator", "btc_wallet_balance", "usd_wallet_balance"]


class CreatorPublicInfoSerializer(serializers.ModelSerializer):
    """Serializer for creator-specific info to be nested in CreatorPublicProfileSerializer"""
    usd_subscription_fee = serializers.SerializerMethodField()
    btc_subscription_fee = serializers.SerializerMethodField()

    def get_usd_subscription_fee(self, obj):
        return str(convert_currency(obj.subscription_fee_currency, "usd", obj.subscription_fee_amount))

    def get_btc_subscription_fee(self, obj):
        return str(convert_currency(obj.subscription_fee_currency, "btc", obj.subscription_fee_amount))

    class Meta:
        model = CreatorInfo
        fields = ["usd_subscription_fee", "btc_subscription_fee"]


class CreatorPublicProfileSerializer(UserDetailsSerializer):
    """Serializer for creator's profile view as seen by other users"""

    profile_photo = CustomImageFieldSerializer(sizes="profile_photo", allow_null=True)
    cover_photo = CustomImageFieldSerializer(sizes="cover_photo", allow_null=True)

    creatorinfo = CreatorPublicInfoSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "public_id", "display_name", "bio", "profile_photo", "cover_photo", "creatorinfo"]


class CreatorPrivateInfoSerializer(serializers.ModelSerializer):
    """Serializer for creator-specific info to be nested in CreatorPrivateProfileSerializer"""
    class Meta:
        model = CreatorInfo
        fields = ["is_verified", "subscription_fee_currency", "subscription_fee_amount", "subscribers_number"]
        read_only_fields = ["is_verified", "subscribers_number"]


class CreatorPrivateProfileSerializer(UserDetailsSerializer):
    """Serializer for creator's profile view as seen by the creator"""

    profile_photo = CustomImageFieldSerializer(sizes="profile_photo", allow_null=True)
    cover_photo = CustomImageFieldSerializer(sizes="cover_photo", allow_null=True)

    creatorinfo = CreatorPrivateInfoSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "public_id", "display_name", "bio", "is_creator", "profile_photo", "cover_photo", "btc_wallet_balance", "usd_wallet_balance", "creatorinfo"]
        read_only_fields = ["public_id", "is_creator", "btc_wallet_balance", "usd_wallet_balance", "creatorinfo"]

    def validate_username(self, value):
        user = self.context['request'].user
        if get_user_model().objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.username = validated_data["username"]
        instance.display_name = validated_data["display_name"]
        instance.bio = validated_data["bio"]
        if validated_data["profile_photo"]:
            instance.profile_photo = validated_data["profile_photo"]
        if validated_data["cover_photo"]:
            instance.cover_photo = validated_data["cover_photo"]

        instance.save()
        return instance
        