from django.contrib.auth import get_user_model

from .base import BaseFeedView
from utils.paginations import CustomCursorPagination as Pagination
from posts.serializers import PostDetailSerializer
from posts.models import Post


class BaseProfilePostFeedView(BaseFeedView):
    """Base feed for all profile post feed views to extend"""

    serializer_class = PostDetailSerializer
    word_fields = ["caption", "uploader__username", "uploader__display_name"]


class ActiveSubPostFeedView(BaseProfilePostFeedView):
    """Active subscriptions post feed view"""

    ordering_fields = ["-upload_time"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        subscriptions = get_user_model().objects.filter(subscribers=user)

        return Post.objects.filter(uploader__in=subscriptions).order_by("-upload_time")


class ExpiredSubPostFeedView(BaseProfilePostFeedView):
    """Expired subscriptions post feed view"""

    ordering_fields = ["-upload_time"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        subscriptions = get_user_model().objects.filter(cancelled_subscribers=user)

        return Post.objects.filter(uploader__in=subscriptions).order_by("-upload_time")


class PurchasedPostFeedView(BaseProfilePostFeedView):
    """Purchased post feed view"""

    ordering_fields = ["-purchase__time_of_purchase"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user

        return Post.objects.filter(buyers=user).order_by("-purchase__time_of_purchase")


class SavedPostFeedView(BaseProfilePostFeedView):
    """Saved post feed view"""

    ordering_fields = ["-videosave__created"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user

        return Post.objects.filter(saves=user).order_by("-videosave__created")
