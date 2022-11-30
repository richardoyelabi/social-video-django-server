from django.contrib.auth import get_user_model
from rest_framework.filters import OrderingFilter

from .base import BaseFeedView
from utils.paginations import CustomCursorPagination as Pagination
from posts.serializers import PostDetailSerializer
from posts.models import Post


class BaseCreatorPostFeedView(BaseFeedView):
    """Base feed for all creator post feed views to extend"""

    serializer_class = PostDetailSerializer


class NewCreatorPostFeedView(BaseCreatorPostFeedView):
    """Creator's new post feed view"""

    filter_backends = [OrderingFilter]
    ordering_fields = ["-upload_time"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):

        creator_id = self.kwargs.get("creator_id")
        creator = get_user_model().objects.get(public_id=creator_id)
        
        return Post.objects.filter(
            uploader = creator
        ).order_by("-upload_time")


class NewCreatorPremiumVideoFeedView(BaseCreatorPostFeedView):
    """Creator's new premium video feed view"""

    filter_backends = [OrderingFilter]
    ordering_fields = ["-upload_time"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):

        creator_id = self.kwargs.get("creator_id")
        creator = get_user_model().objects.get(public_id=creator_id)
        
        return Post.objects.filter(
            uploader = creator,
            post_type = "paid_video"
        ).order_by("-upload_time")


class TopCreatorPremiumVideoFeedView(BaseCreatorPostFeedView):
    """Creator's top premium video feed view"""

    filter_backends = [OrderingFilter]
    ordering_fields = ["-feed_score"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):

        user = self.request.user

        creator_id = self.kwargs.get("creator_id")
        creator = get_user_model().objects.get(public_id=creator_id)

        return Post.objects.filter(
            uploader = creator,
            post_type = "paid_video"
        ).exclude(
            uniqueview__account = user
        ).order_by("-feed_score")
