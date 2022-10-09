from django.contrib import admin
from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "uploader",
        "content_type",
        "upload_time",
        "image",
    )

admin.site.register(Photo, PhotoAdmin)
