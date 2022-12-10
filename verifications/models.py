from django.db import models
from versatileimagefield.fields import VersatileImageField

from django.conf import settings
from media.media_paths import upload_id_path

import uuid


class IdUpload(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="id_uploads", on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[
        ("selfie", "Selfie"), 
        ("doc", "Passport/ Id card")
    ])
    upload_time = models.DateTimeField(auto_now_add=True)
    upload = VersatileImageField(upload_to=upload_id_path)

    def __str__(self) -> str:
        return f"{self.creator.username}'s id upload {self.public_id}"