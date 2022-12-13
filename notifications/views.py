from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import status

from utils.paginations import CustomCursorPagination as Pagination
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationListView(ListAPIView):

    serializer_class = NotificationSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["-timestamp"]
    ordering = ordering_fields[0]
    pagination_class = Pagination
    
    def get_queryset(self):
        user = self.request.user
        return  Notification.objects.filter(receiver=user)

    def list(self, request, *args, **kwargs):
        
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        def get_data(instances):
            queryset = []
            for instance in instances:

                notification = Notification.format(instance.record)

                notification["public_id"] = instance.public_id
                notification["timestamp"] = instance.timestamp

                queryset.append(notification)

            return queryset

        if page is not None:
            page = get_data(page)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            queryset = get_data(queryset)
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NotificationSeenView(APIView):

    def post(self, request, *args, **kwargs):

        account = request.user
        account.notification_seen = True
        account.save(update_fields=["notification_seen"])

        return Response("Notification view acknowledged", status.HTTP_202_ACCEPTED)