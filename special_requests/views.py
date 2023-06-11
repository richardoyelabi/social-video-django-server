from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from special_requests.models import MessagePurchase
from special_requests.serializers import MessagePurchaseSerializer
from chats.models import ChatMessage
from transactions.exceptions import TransactionInsufficientBalanceError


class MessagePurchaseView(GenericAPIView):
    """Purchase a message video.
    Accepts POST."""

    queryset = MessagePurchase.objects.all()
    serializer_class = MessagePurchaseSerializer
    lookup_url_kwarg = "message_id"

    def post(self, request, message_id, *args, **kwargs):
        buyer = request.user
        message = ChatMessage.objects.get(public_id=message_id)

        if message.message_type != "paid_video":
            return Response(
                "Media doesn't require purchase", status.HTTP_400_BAD_REQUEST
            )

        if MessagePurchase.objects.filter(buyer=buyer, video_message=message).exists():
            return Response(
                "User already unlocked the video.", status.HTTP_400_BAD_REQUEST
            )

        try:
            currency = request.data["currency"]
        except KeyError:
            return Response(
                "Provide valid 'currency' parameter: currency is either 'usd' or 'btc'."
            )

        if not currency in ("btc", "usd"):
            return Response(
                "Provide valid 'currency' parameter: currency is either 'usd' or 'btc'."
            )

        try:
            MessagePurchase.objects.create(
                buyer=buyer, video_message=message, fee_currency=currency
            )
        except TransactionInsufficientBalanceError as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)

        return Response("Video unlocked.", status.HTTP_201_CREATED)
