from django.contrib.auth import get_user_model

from .base import BaseFeedView
from utils.paginations import CustomCursorPagination as Pagination
from accounts.serializers import CreatorPublicProfileSerializer


class BaseCreatorFeedView(BaseFeedView):
    """Base feed for all creator feed views to extend"""

    serializer_class = CreatorPublicProfileSerializer
    word_fields = ["username", "display_name"]


class TopCreatorFeedView(BaseCreatorFeedView):
    """Top creator feed (by number of subscribers) view"""

    ordering_fields = ["-creatorinfo__subscribers_number"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):

        user = self.request.user

        return get_user_model().objects.filter(
            is_creator = True
        ).exclude(
            subscribers__id = user.id
        ).order_by("-creatorinfo__subscribers_number")


class SugCreatorFeedView(BaseCreatorFeedView):
    """Hot creator feed (by post engagement) view"""

    ordering_fields = ["-creatorinfo__feed_score"]
    ordering = ordering_fields[0]
    pagination_class = Pagination

    def get_queryset(self):

        user = self.request.user

        return get_user_model().objects.filter(
            is_creator = True
        ).exclude(
            subscribers__id = user.id
        ).order_by("-creatorinfo__feed_score")
