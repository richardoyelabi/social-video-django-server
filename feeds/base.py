from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from rest_framework_word_filter import FullWordSearchFilter

from utils.paginations import CustomCursorPagination


class BaseFeedView(ListAPIView):
    """
    Base ListAPIView for all feeds to extend.
    Implements basic list and pagination.
    """

    pagination_class = CustomCursorPagination
    filter_backends = [OrderingFilter, FullWordSearchFilter]
    