from django.contrib.contenttypes.models import ContentType
from rest_framework.filters import OrderingFilter

from .base import BaseFeedView
from utils.paginations import CustomCursorPagination as Pagination
from posts.serializers import PostDetailSerializer
from posts.models import Post
from media.models import Video


class BasePostFeedView(BaseFeedView):
    """Base feed for all general post feed views to extend"""

    serializer_class = PostDetailSerializer


class AllPostFeedView(BasePostFeedView):
    """All (home) post feed view"""

    filter_backends = [OrderingFilter]
    ordering_fields = ["-feed_score"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):

        user = self.request.user

        return Post.objects.all(
        ).exclude(
            uniqueview__account = user
        ).order_by("-feed_score")


class TopVideoFeedView(BasePostFeedView):
    """Top video feed view"""

    filter_backends = [OrderingFilter]
    ordering_fields = ["-feed_score"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):

        user = self.request.user

        return Post.objects.filter(
            media_type = ContentType.objects.get_for_model(Video)
        ).exclude(
            uniqueview__account = user
        ).order_by("-feed_score")


class TopPremiumVideoFeedView(BasePostFeedView):
    """Top premium feed view"""

    filter_backends = [OrderingFilter]
    ordering_fields = ["-feed_score"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):

        user = self.request.user

        return Post.objects.filter(
            post_type = "paid_video"
        ).exclude(
            uniqueview__account = user
        ).order_by("-feed_score")


class NewPremiumVideoFeedView(BasePostFeedView):
    """New premium video feed view"""

    filter_backends = [OrderingFilter]
    ordering_fields = ["-upload_time"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):

        user = self.request.user
        subscriptions = user.subscriptions.all()

        return Post.objects.filter(
            post_type = "paid_video",
            uploader__in = subscriptions
        ).exclude(
            uniqueview__account = user
        ).order_by("-upload_time")
