from django.contrib import admin

from .models import Post, Like, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "uploader",
        "post_type",
        "upload_time",
        "caption",
        "media_item",
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

admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
