from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AccountCreationForm, AccountChangeForm
from .models import Account

class AccountAdmin(UserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm
    model = Account
    list_display = [
        "email",
        "username",
        "is_staff",
        "display_name", 
        "bio", 
        "profile_photo", 
        "cover_photo",
        "notification_settings",
        "is_creator"
        ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            ("Personal info"), 
            {
                "fields": (
                    "display_name",
                    "email",
                    "bio",
                    "profile_photo",
                    "cover_photo",
                    "is_creator",
                    "notification_settings",
                )
            }
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


    add_fieldsets = UserAdmin.add_fieldsets

admin.site.register(Account, AccountAdmin)
