from django.contrib import admin

from .models import IdUpload


class IdUploadAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "creator",
        "type",
        "upload_time",
        "upload",
    )


admin.site.register(IdUpload, IdUploadAdmin)