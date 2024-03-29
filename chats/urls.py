from django.urls import path, include
from chats.views import (
    InboxListView,
    InboxReadView,
    InboxMessageView,
    UserInboxView,
    ChatContactsList,
    MessageVideoStreamView,
)

urlpatterns = [
    path("inbox/<uuid:contact_id>/read/", InboxReadView.as_view(), name="inbox_read"),
    path("inbox/", InboxListView.as_view({"get": "list"}), name="inbox"),
    path(
        "message/<uuid:message_id>/video-stream/<uuid:video_id>/",
        MessageVideoStreamView.as_view(),
        name="message_video_stream",
    ),
    path(
        "messages/<uuid:public_id>/",
        InboxMessageView.as_view({"get": "list"}),
        name="inbox_message",
    ),
    path(
        "account/<uuid:public_id>/",
        UserInboxView.as_view({"get": "retrieve"}),
    ),
    path("contacts/", ChatContactsList.as_view(), name="chat_contacts"),
    # Vault
    path("vault/", include("chats.media_vault.urls")),
]
