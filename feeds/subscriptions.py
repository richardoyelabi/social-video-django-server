from rest_framework.generics import ListAPIView

from posts.serializers import PhotoPostDetailSerializer, VideoPostDetailSerializer, PaidVideoPostDetailSerializer
from accounts.serializers import CreatorPublicProfileSerializer


class ActiveSubListView(ListAPIView):
    """Active subscriptions feed"""

