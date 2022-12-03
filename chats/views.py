from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework_word_filter import FullWordSearchFilter
from channels.layers import get_channel_layer

from chats.serializers import AccountChatSerializer, MessageListSerializer
from chats.models import Inbox, ChatMessage
from media.models import Video
from special_requests.models import MessagePurchase
from chats.serializers import InboxSerializer
from utils.paginations import CustomCursorPagination
from sage_stream.api.views import VideoStreamAPIView

channel_layer = get_channel_layer()
User = get_user_model()


class UserInboxView(ModelViewSet):
    serializer_class = AccountChatSerializer
    permission_classes = [IsAuthenticated]

    @action(methods='get', detail=True)
    def retrieve(self, request, *args, **kwargs):
        try:
            user_profile = User.objects.get(public_id=self.kwargs.get('public_id'))
            serializer = self.serializer_class(instance=user_profile, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


class InboxMessageView(ModelViewSet):
    serializer_class = MessageListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'public_id'
    filter_backends = [FullWordSearchFilter]
    word_fields = ["message"]

    class Pagination(CustomCursorPagination):
        ordering = "-timestamp"

    pagination_class = Pagination

    def get_queryset(self):
        try:
            inbox = Inbox.objects.get(user=self.request.user, second__public_id=self.kwargs.get('public_id'))
            return ChatMessage.objects.filter(inbox=inbox).order_by('-timestamp')
        except Inbox.DoesNotExist:
            return Inbox.objects.none()


class InboxListView(ModelViewSet):
    serializer_class = InboxSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [FullWordSearchFilter]
    word_fields = ["second__username", "second__display_name"]

    class Pagination(CustomCursorPagination):
        ordering = "-updated"

    pagination_class = Pagination

    def get_queryset(self):
        return Inbox.objects.filter(user=self.request.user).order_by('-updated')


class ChatContactsList(ListAPIView):
    serializer_class = AccountChatSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [FullWordSearchFilter]
    word_fields = ["username", "display_name"]

    class Pagination(CustomCursorPagination):
        ordering = "username"

    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user

        if user.is_creator:
            return user.subscribers.all()
        return user.subscriptions.all()


class MessageVideoStreamView(VideoStreamAPIView):
    """Stream message video.
    Accepts GET"""

    def get(self, request, message_id, video_id, *args, **kwargs):
        """Authorize user to view stream and call super() to send stream"""

        message = ChatMessage.objects.get(public_id=message_id)
        video = Video.objects.get(public_id=video_id)

        error_response = Response("You're not authorized to watch this video. Please, unlock video to watch.", 
            status=status.HTTP_401_UNAUTHORIZED)

        if message.media_item != video:
            return error_response

        user = request.user
        creator = message.user

        if message.message_type=="free_video" or \
            MessagePurchase.objects.filter(buyer=user, video_message=message).exists() or \
                user==creator:

                return super().get(request, video_id)

        return error_response
