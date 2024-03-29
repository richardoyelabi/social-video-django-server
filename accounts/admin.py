from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AccountCreationForm, AccountChangeForm
from .models import Account, CreatorInfo


class AccountAdmin(UserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm
    model = Account
    list_display = [
        "id",
        "email",
        "username",
        "is_staff",
        "display_name",
        "active_subscriptions_number",
        "expired_subscriptions_number",
        "bio",
        "profile_photo",
        "cover_photo",
        "is_creator",
        "public_id",
        "saved_videos_number",
        "purchased_videos_number",
        "btc_wallet_balance",
        "usd_wallet_balance",
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
                )
            },
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

    add_fieldsets = (
        (
            None,
            {"fields": ("username", "email", "is_creator", "password1", "password2")},
        ),
    )


class CreatorInfoAdmin(admin.ModelAdmin):
    @admin.display(description="Creator username")
    def username(self, obj):
        return obj.creator.username

    @admin.display(description="Public Id")
    def public_id(self, obj):
        return obj.creator.public_id

    list_display = (
        "creator",
        "public_id",
        "subscribers_number",
        "subscription_fee_currency",
        "subscription_fee_amount",
        "is_verified",
        "identity",
        "feed_score",
    )

    fields = (
        "creator",
        "is_verified",
        "identity",
    )

    search_fields = (
        "creator__username",
        "creator__public_id",
    )


admin.site.register(Account, AccountAdmin)
admin.site.register(CreatorInfo, CreatorInfoAdmin)
