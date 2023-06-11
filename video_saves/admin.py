from django.contrib import admin
from video_saves.models import VideoSave


class VideoSaveAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "video_post",
        "created",
    )


admin.site.register(VideoSave, VideoSaveAdmin)
