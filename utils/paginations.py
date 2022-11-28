from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    page_size_query_param = "size"


class PostCommentViewPagination(CustomCursorPagination):
    ordering = "time"


class InboxMessagePagination(CustomCursorPagination):
    ordering = "-timestamp"


class InboxListPagination(CustomCursorPagination):
    ordering = "-updated"


class ChatContactsListPagination(CustomCursorPagination):
    ordering = "username"

class BaseFeedViewPagination(CustomCursorPagination):
    page_size_query_param = "size"