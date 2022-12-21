from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Account

class AccountCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Account
        fields = UserCreationForm.Meta.fields + (
            "display_name", 
            "is_creator",
            "is_staff",
            )

class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        #fields = UserChangeForm.Meta.fields
        fields = (
            "username",
            "email",
            "password",
            "display_name", 
            "bio", 
            "profile_photo", 
            "cover_photo",
            "payment_info",
            "is_creator",
            "is_staff",
            )