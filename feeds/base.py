from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from utils.paginations import BaseFeedViewPagination


class BaseFeedView(ListAPIView):
    """
    Base ListAPIView for all feeds to extend.
    Implements basic list and pagination.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = BaseFeedViewPagination

    