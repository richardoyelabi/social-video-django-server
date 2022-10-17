from pathlib import Path

def profile_photos_path(instance, filename):
    file_extension = Path(filename).suffix
    return f"profile_photos/{instance.username}/{instance.public_id}_ProfilePhoto_{instance.username}{file_extension}"

def cover_photos_path(instance, filename):
     file_extension = Path(filename).suffix
     return f"cover_photos/{instance.username}/{instance.public_id}_CoverPhoto_{instance.username}{file_extension}"

def photo_uploads_path(instance, filename):
     file_extension = Path(filename).suffix
     return f"photo_uploads/{instance.uploader.username}/{instance.public_id}_PhotoUpload_{instance.uploader.username}{file_extension}"

def video_uploads_path(instance, filename):
     file_extension = Path(filename).suffix
     return f"video_uploads/{instance.uploader.username}/{instance.public_id}_VideoUpload_{instance.uploader.username}{file_extension}"
