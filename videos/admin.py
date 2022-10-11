from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "uploader",
        "content_type",
        "upload_time",
        "video",
    )

admin.site.register(Video, VideoAdmin)
