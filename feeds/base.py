from rest_framework.generics import ListAPIView

from utils.paginations import CustomCursorPagination


class BaseFeedView(ListAPIView):
    """
    Base ListAPIView for all feeds to extend.
    Implements basic list and pagination.
    """

    pagination_class = CustomCursorPagination

    