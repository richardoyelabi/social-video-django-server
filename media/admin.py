from django.contrib import admin
from .models import Photo, Video

class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "uploader",
        "content_type",
        "upload_time",
        "media",
    )

class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "uploader",
        "content_type",
        "upload_time",
        "media",
    )

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Video, VideoAdmin)
