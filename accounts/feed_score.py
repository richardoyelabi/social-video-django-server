from posts.models import Like, UniqueView

from datetime import datetime, timedelta


def creator_feed_score_update(instance, created):
    """
    Update feed_score field of instance.post when instance is created.
    Instance may be posts.Like, posts.UniqueView, etc.
    """

    if created:
        time_frame = timedelta(days=7)  # Time frame to use when computing feed_score

        start_time = datetime.now() - time_frame

        creator = instance.post.uploader

        likes = Like.objects.filter(post__uploader=creator, time__gte=start_time)

        likes_number = likes.count()

        views = UniqueView.objects.filter(post__uploader=creator, time__gte=start_time)

        views_number = views.count()

        feed_score = likes_number / views_number

        creator.creatorinfo.feed_score = feed_score
        creator.creatorinfo.save(update_fields=["feed_score"])
