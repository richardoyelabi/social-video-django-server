from django.contrib import admin

from .models import IdUpload


class IdUploadAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "creator",
        "reviewed",
        "type",
        "upload_time",
        "upload",
    )

    fields = ("reviewed",)

    search_fields = (
        "creator__username",
        "creator__public_id",
    )


admin.site.register(IdUpload, IdUploadAdmin)
