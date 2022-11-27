from rest_framework.pagination import CursorPagination


class InboxMessagePagination(CursorPagination):
    ordering = "-timestamp"


class InboxListPagination(CursorPagination):
    ordering = "-updated"


class ChatContactsListPagination(CursorPagination):
    ordering = "username"

class BaseFeedViewPagination(CursorPagination):
    page_size_query_param = "size"