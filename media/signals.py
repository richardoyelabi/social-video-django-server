from django_cleanup.signals import cleanup_pre_delete
from versatileimagefield.fields import VersatileImageField
from videothumbs.fields import VideoThumbnailField
import os

from django.conf import settings


def delete_thumbnails(**kwargs):
    """Delete thumbnails of media files
    before django_cleanup deletes the parent files"""

    file = kwargs["file"]

    if isinstance(file.field, VersatileImageField):
        file.delete_all_created_images()

    elif isinstance(file.field, VideoThumbnailField):
        media_dir = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        rel_url = file.url_300x300
        rel_url = rel_url.replace(media_url, media_dir)

        url = os.path.join(media_dir, rel_url)

        file.storage.delete(url)


cleanup_pre_delete.connect(delete_thumbnails)
