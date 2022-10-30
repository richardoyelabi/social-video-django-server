from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete
from media.exceptions import MediaUseError
from .models import Post, Like, Comment

@receiver(pre_save, sender=Post)
def check_media_ownership(sender, instance, **kwargs):
    """Make sure accounts can not use media items that do not belong to them in a post"""

    if (instance.media_item.uploader != instance.uploader):
        raise MediaUseError("This account does not have permission to use the media in this post.")

#@receiver(pre_save, sender=Post)
#def check_media_consistency(sender, instance, **kwargs):
#    """Make sure photo media doesn't get into video posts and vice versa"""
#
#    if not(instance.post_type=="photo" and instance.media_type.model=="photo") \
#        or not((instance.post_type=="free_video" or instance.post_type=="paid_video" )and instance.media_type.model=="video"):
#        raise MediaUseError("Post type does not match media type. Please, correct the discrepancy.")

@receiver(post_save, sender=Like)
def increase_likes_number(sender, instance, created, **kwargs):
    """Increase post's likes_number for each new like"""

    if created:
        instance.post.likes_number += 1
        instance.post.save(update_fields=["likes_number"])

@receiver(pre_delete, sender=Like)
def decrease_likes_number(sender, instance, **kwargs):
    """Decrease post's likes_number for each deleted like"""

    instance.post.likes_number -= 1
    instance.post.save(update_fields=["likes_number"])

@receiver(post_save, sender=Comment)
def increase_comments_number(sender, instance, created, **kwargs):
    """Increase post's comments_number for each new comment"""

    if created:
        instance.post.comments_number += 1
        instance.post.save(update_fields=["comments_number"])

@receiver(pre_delete, sender=Comment)
def decrease_comments_number(sender, instance, **kwargs):
    """Decrease post's comments_number for each deleted comment"""

    instance.post.comments_number -= 1
    instance.post.save(update_fields=["comments_number"])
