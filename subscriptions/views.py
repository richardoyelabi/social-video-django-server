from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from subscriptions.models import Subscription
from accounts.models import CreatorInfo
from subscriptions.serializers import SubscriptionSerializer, SetSubscriptionSerializer
from .permissions import IsCreator
from transactions.models import Transaction
from transactions.exceptions import TransactionInsufficientBalanceError


class SubscriptionView(GenericAPIView):
    """Subscribe or unsubscribe to a creator.
    POST to subscribe; DELETE to unsubscribe."""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    lookup_url_kwarg = "creator_id"

    def post(self, request, creator_id, *args, **kwargs):
        Account = get_user_model()
        subscribed_to = Account.objects.get(public_id=creator_id)
        subscriber = request.user

        if Subscription.objects.filter(
            subscribed_to = subscribed_to,
            subscriber = subscriber
        ).exists():
            return Response("Subscription already exists.", status.HTTP_400_BAD_REQUEST)

        try:
            currency = request.query_params["currency"]
        except KeyError:
            return Response("Provide valid 'currency' get parameter: currency=usd or currency=btc")

        if not currency in ("btc", "usd"):
            return Response("Provide valid 'currency' get parameter: currency=usd or currency=btc")

        try:
            Subscription.objects.create(subscribed_to=subscribed_to, subscriber=subscriber, fee_currency=currency)
        except TransactionInsufficientBalanceError as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)
            
        return Response("Subscription created.", status.HTTP_201_CREATED)

    def delete(self, request, creator_id, *args, **kwargs):
        Account = get_user_model()
        subscribed_to = Account.objects.get(public_id=creator_id)
        subscriber = request.user
        
        if not Subscription.objects.filter(
            subscribed_to = subscribed_to,
            subscriber = subscriber
        ).exists():
            return Response("Subscription does not exist.", status.HTTP_400_BAD_REQUEST)

        Subscription.objects.get(subscribed_to=subscribed_to, subscriber=subscriber).delete()
        return Response("Subscription deleted.", status.HTTP_204_NO_CONTENT)


class SetSubscriptionView(GenericAPIView):
    """Set creator's subscription_fee_currency and subscription_fee_amount.
    Accepts POST with parameters fee_currency and fee_amount"""

    queryset = CreatorInfo.objects.all()
    serializer_class = SetSubscriptionSerializer
    permission_classes = [IsCreator]

    def post(self, request, *args, **kwargs):
        creator = request.user
        creator_id = request.user.public_id

        data = dict(
            creator = creator_id,
            subscription_fee_currency = request.data.get("subscription_fee_currency"),
            subscription_fee_amount = request.data.get("subscription_fee_amount")
        )

        creatorinfo = CreatorInfo.objects.get(creator=creator)

        serializer = SetSubscriptionSerializer(creatorinfo, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)