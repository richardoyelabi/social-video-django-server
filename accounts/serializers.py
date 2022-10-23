from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


from accounts.models import CreatorInfo

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
    class Meta:
        model = get_user_model()
        fields = ["username", "display_name", "bio", "profile_photo", "cover_photo"]

class UserPrivateProfileSerializer(UserDetailsSerializer):
    """Serializer for non-creator user's profile view as seen by the user"""
    class Meta:
        model = get_user_model()
        fields = ["username", "display_name", "bio", "profile_photo", "cover_photo", "btc_wallet_balance", "usd_wallet_balance"]
        read_only_fields = ["btc_wallet_balance", "usd_wallet_balance"]

class CreatorPublicInfoSerializer(serializers.ModelSerializer):
    """Serializer for creator-specific info to be nested in CreatorPublicProfileSerializer"""
    class Meta:
        model = CreatorInfo
        fields = ["subscription_fee_currency", "subscription_fee_amount"]

class CreatorPublicProfileSerializer(UserDetailsSerializer):
    """Serializer for creator's profile view as seen by other users"""
    creator_info = CreatorPublicInfoSerializer()
    class Meta:
        model = get_user_model()
        fields = ["username", "display_name", "bio", "profile_photo", "cover_photo", "creator_info"]

class CreatorPrivateInfoSerializer(serializers.ModelSerializer):
    """Serializer for creator-specific info to be nested in CreatorPrivateProfileSerializer"""
    class Meta:
        model = CreatorInfo
        fields = ["subscription_fee_currency", "subscription_fee_amount", "subscribers_number"]
        read_only_fields = ["subscription_fee_currency", "subscription_fee_amount", "subscribers_number"]

class CreatorPrivateProfileSerializer(UserDetailsSerializer):
    """Serializer for creator's profile view as seen by the creator"""
    creator_info = CreatorPublicInfoSerializer()
    class Meta:
        model = get_user_model()
        fields = ["username", "display_name", "bio", "profile_photo", "cover_photo", "btc_wallet_balance", "usd_wallet_balance", "creator_info"]
        read_only_fields = ["btc_wallet_balance", "usd_wallet_balance"]