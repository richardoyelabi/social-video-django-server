from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import status

from utils.paginations import CustomCursorPagination as Pagination
from notifications.models import Notification
from notifications.serializers import NotificationSerializer, NotificationSettingsListSerializer


class NotificationListView(ListAPIView):
    """Retrieve list of notifications.
    Accepts GET"""

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
    """Send acknowledgement that notification has been seen.
    Accepts POST"""

    def post(self, request, *args, **kwargs):

        account = request.user
        account.notification_seen = True
        account.save(update_fields=["notification_seen"])

        return Response("Notification view acknowledged", status.HTTP_202_ACCEPTED)


class NotificationSettingView(APIView):
    """Activate or deactivate notification settings.
    Which setting to update is determined by the request path.
    Accepts POST and DELETE"""

    def post(self, request, *args, **kwargs):

        account = request.user
        setting = self.get_setting(request.path, account)

        if setting["value"]:
            return Response(f"{setting['name']} setting is already activated", status.HTTP_208_ALREADY_REPORTED)

        exec(f"account.{setting['name']} = True")

        account.save(update_fields=[setting['name']])

        return Response(f"{setting['name']} setting activated", status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        account = request.user
        setting = self.get_setting(request.path, account)

        if not setting["value"]:
            return Response(f"{setting['name']} setting is already deactivated", status.HTTP_208_ALREADY_REPORTED)

        exec(f"account.{setting['name']} = False")

        account.save(update_fields=[setting['name']])

        return Response(f"{setting['name']} setting deactivated", status.HTTP_200_OK)

    def get_setting(self, path, account):
        """Get the notification setting to be updated from url"""

        match path:

            case "/notification/setting/site/messages/":

                return dict(
                    name = "site_message",
                    value = account.site_message
                )

            case "/notification/setting/site/promotions/":

                return dict(
                    name="site_promotion",
                    value=account.site_promotion
                )

            case "/notification/setting/email/messages/":

                return dict(
                    name = "email_message",
                    value = account.email_message
                )

            case "/notification/setting/email/promotions/":

                return dict(
                    name = "email_promotion",
                    value = account.email_promotion
                )


class NotificationSettingsListView(APIView):
    """Retrieve all notification settings.
    Accepts GET"""

    def get(self, request, *args, **kwargs):

        account = request.user

        serializer = NotificationSettingsListSerializer(account)

        return Response(serializer.data, status.HTTP_200_OK)