from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from video_saves.models import VideoSave
from posts.exceptions import PostTypeError

#Confirm that post is a video before allowing video save
@receiver(pre_save, sender=VideoSave)
def confirm_saved_post_is_video(sender, instance, **kwargs):
    """Confirm that post is a video before allowing video save"""

    if not (instance.video_post.post_type=="free_video" or instance.video_post.post_type=="paid_video"):
        raise PostTypeError("Only video posts can be saved.")
        
#Update saved_videos_number when videos are saved
@receiver(post_save, sender=VideoSave)
def increase_saved_videos_number(sender, instance, created, **kwargs):
    """Update saved_videos_number when videos are saved"""

    #Increase user's saved_videos_number for each new video save
    if created:
        instance.account.saved_videos_number += 1
        instance.account.save(update_fields=["saved_videos_number"])

#Update saved_videos_number when videos are unsaved
@receiver(pre_delete, sender=VideoSave)
def decrease_saved_videos_number(sender, instance, **kwargs):
    """Update saved_videos_number when videos are unsaved"""

    #Decrease user's saved_videos_number for each undone video save
    instance.account.saved_videos_number -= 1
    instance.account.save(update_fields=["saved_videos_number"])
