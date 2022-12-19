from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete
from django.core.files import File

from media.models import Photo, Video
from media.exceptions import MediaUseError
from .models import Post, Like, Comment, View, UniqueView
from .feed_score import feed_score_update
from accounts.feed_score import creator_feed_score_update
from utils.video_preview import cut_video_preview, clean_temp
from notifications.models import Notification

from pathlib import Path

#Make sure accounts can not use media items that do not belong to them in a post
@receiver(pre_save, sender=Post)
def check_media_ownership(sender, instance, **kwargs):

    if (instance.media_item.uploader != instance.uploader):
        raise MediaUseError("This account does not have permission to use the media in this post.")


#Make sure photo media doesn't get into video posts and vice versa
@receiver(pre_save, sender=Post)
def check_media_consistency(sender, instance, **kwargs):

    if not(
        instance.post_type == "photo" 
        and 
        instance.media_type == ContentType.objects.get_for_model(Photo)
    ) \
    \
    and not(
        (
            instance.post_type=="free_video" or instance.post_type=="paid_video"
        )
        and 
        instance.media_type == ContentType.objects.get_for_model(Video)
    ):

        raise MediaUseError("Post type does not match media type. Please, correct the discrepancy.")


#Make sure no premium video has non-zero purchase amount
@receiver(pre_save, sender=Post)
def assert_premium_status(sender, instance, **kwargs):

    if instance.post_type=="paid_video":
        if instance.purchase_cost_amount<=0:
            instance.post_type = "free_video"
            instance.save(update_fields=["post_type"])


#Create preview for premium videos in premium video posts
@receiver(post_save, sender=Post)
def create_video_preview(sender, instance, created, **kwargs):

    if instance.post_type=="paid_video" and not instance.video_preview:

        temp_path = cut_video_preview(instance.media_item.media.path)
        path = Path(temp_path)

        with path.open("rb") as f:
            instance.video_preview = File(f, name=path.name)
            instance.save(update_fields=["video_preview"])
            
        clean_temp(temp_path)


#Increase post's likes_number for each new like
@receiver(post_save, sender=Like)
def increase_likes_number(sender, instance, created, **kwargs):

    if created:
        instance.post.likes_number += 1
        instance.post.save(update_fields=["likes_number"])


#Decrease post's likes_number for each deleted like
@receiver(pre_delete, sender=Like)
def decrease_likes_number(sender, instance, **kwargs):

    instance.post.likes_number -= 1
    instance.post.save(update_fields=["likes_number"])


#Increase post's comments_number for each new comment
@receiver(post_save, sender=Comment)
def increase_comments_number(sender, instance, created, **kwargs):

    if created:
        instance.post.comments_number += 1
        instance.post.save(update_fields=["comments_number"])


#Decrease post's comments_number for each deleted comment
@receiver(pre_delete, sender=Comment)
def decrease_comments_number(sender, instance, **kwargs):

    instance.post.comments_number -= 1
    instance.post.save(update_fields=["comments_number"])


#If user is viewing post for the first time, record the view in unique_view table
@receiver(post_save, sender=View)
def record_unique_view(sender, instance, created, **kwargs):
    """If View instance doesn't exist in UniqueView, duplicate View instance in UniqueView"""

    if created:
        if not UniqueView.objects.filter(
            account = instance.account,
            post = instance.post
        ).exists():
            UniqueView.objects.create(
                account = instance.account,
                post = instance.post,
                time = instance.time
            )


#Increase post's views_number for each new View instance
@receiver(post_save, sender=View)
def increase_views_number(sender, instance, created, **kwargs):

    if created:
        instance.post.views_number += 1
        instance.post.save(update_fields=["views_number"])


#Increase post's unique_views_number for each new UniqueView instance
@receiver(post_save, sender=UniqueView)
def increase_unique_views_number(sender, instance, created, **kwargs):

    if created:
        instance.post.unique_views_number += 1
        instance.post.save(update_fields=["unique_views_number"])


#Update post's feed_score when there's a new UniqueView instance
@receiver(post_save, sender=UniqueView)
def feed_score_view_update(sender, instance, created, **kwargs):
    
    feed_score_update(instance, created)


#Update post's feed_score when there's a new Like instance
@receiver(post_save, sender=Like)
def feed_score_like_update(sender, instance, created, **kwargs):

    feed_score_update(instance, created)


#Update creator's feed_score when there's a new UniqueView instance
@receiver(post_save, sender=UniqueView)
def creator_feed_score_view_update(sender, instance, created , **kwargs):

    creator_feed_score_update(instance, created)


#Update creator's feed_score when there's a new Like instance
@receiver(post_save, sender=Like)
def creator_feed_score_like_update(sender, instance, created , **kwargs):

    creator_feed_score_update(instance, created)


#Notify post uploader of like
@receiver(post_save, sender=Like)
def like_notify(sender, instance, created, **kwargs):

    if created:

        receiver = instance.post.uploader
        record = instance

        Notification.notify(receiver=receiver, record=record)


#Notify post uploader of comment
@receiver(post_save, sender=Comment)
def comment_notify(sender, instance, created, **kwargs):

    if created:

        receiver = instance.post.uploader
        record = instance

        Notification.notify(receiver=receiver, record=record)