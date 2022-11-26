from datetime import datetime, timedelta

def feed_score_update(instance, created):
    """
    Update feed_score field of instance.post when instance is created.
    Instance may be posts.Like, posts.UniqueView, etc.
    """

    if created:

        time_frame = timedelta(days=7) #Time frame to use when computing feed_score

        start_time = datetime.now() - time_frame

        post = instance.post

        likes = post.liked_by.filter(time=start_time)
        likes_number = likes.count()

        views = post.unique_viewers.filter(time=start_time)
        views_number = views.count()

        feed_score = likes_number / views_number

        post.feed_score = feed_score
        post.save(update_fields=["feed_score"])