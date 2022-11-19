from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from channels.layers import get_channel_layer

from chats.serializers import AccountChatSerializer, MessageListSerializer
from chats.models import Inbox, ChatMessage
from chats.serializers import InboxSerializer
from utils.paginations import InboxMessagePagination, InboxListPagination, ChatContactsListPagination
from subscriptions.models import Subscription

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
    pagination_class = InboxMessagePagination
    lookup_field = 'public_id'

    def get_queryset(self):
        try:
            inbox = Inbox.objects.get(user=self.request.user, second__public_id=self.kwargs.get('public_id'))
            return ChatMessage.objects.filter(inbox=inbox).order_by('-timestamp')
        except Inbox.DoesNotExist:
            return Inbox.objects.none()


class InboxListView(ModelViewSet):
    serializer_class = InboxSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = InboxListPagination

    def get_queryset(self):
        return Inbox.objects.filter(user=self.request.user).order_by('-updated')


class ChatContactsList(ListAPIView):
    serializer_class = AccountChatSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ChatContactsListPagination

    def get_queryset(self):
        user = self.request.user

        #return user.subscriptions.all()
        if user.is_creator:
            return user.subscribers.all()
        return user.subscriptions.all()
