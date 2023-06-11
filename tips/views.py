from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from tips.models import Tip
from tips.serializers import TipSerializer
from transactions.exceptions import TransactionInsufficientBalanceError


class TipView(GenericAPIView):
    """Send a tip.
    Accepts POST"""

    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    lookup_url_kwarg = "creator_id"

    def post(self, request, creator_id, *args, **kwargs):
        sender = request.user.id
        receiver = get_user_model().objects.get(public_id=creator_id).id
        fee_currency = request.data.get("fee_currency")
        fee_amount = request.data.get("fee_amount")

        if not (fee_currency and fee_amount):
            return Response(
                "'fee_currency' or 'fee_amount' is missing.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "sender": sender,
            "receiver": receiver,
            "fee_currency": fee_currency,
            "fee_amount": fee_amount,
        }

        serializer = TipSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
            except TransactionInsufficientBalanceError as e:
                return Response(str(e), status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
