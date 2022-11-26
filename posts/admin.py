from django.contrib import admin

from .models import Post, Like, Comment, View, UniqueView

class PostAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "uploader",
        "post_type",
        "upload_time",
        "caption",
        "media_item",
        "feed_score",
        "purchase_cost_currency",
        "purchase_cost_amount",
    )

class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "post",
        "time",
    )

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "comment_text",
        "post",
        "time",
    )

class ViewAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "post",
        "time"
    )

class UniqueViewAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "post",
        "time"
    )

admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(UniqueView, UniqueViewAdmin)
