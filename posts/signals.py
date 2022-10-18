from django.dispatch import receiver
from django.db.models.signals import pre_save
from media.exceptions import MediaUseError
from .models import Post

@receiver(pre_save, sender=Post)
def check_media_ownership(sender, instance, **kwargs):
    """Make sure accounts can not use media items that do not belong to them in a post"""
    if (instance.media_item.uploader != instance.uploader):
        raise MediaUseError("This account does not have permission to use the media in this post.")

@receiver(pre_save, sender=Post)
def check_media_consistency(sender, instance, **kwargs):
    """Make sure photo media doesn't get into video posts and vice versa"""
    if not(instance.post_type=="photo" and instance.media_type.model=="photo") \
        or not((instance.post_type=="free_video" or instance.post_type=="paid_video" )and instance.media_type.model=="video"):
        raise MediaUseError("Post type does not match media type. Please, correct the discrepancy.")