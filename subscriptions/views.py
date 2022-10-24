from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer

class SubscriptionView(GenericAPIView):
    """Subscribe or unsubscribe to a creator.
    POST to subscribe; DELETE to unsubscribe."""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    lookup_url_kwarg = "creator_username"

    def post(self, request, creator_username, *args, **kwargs):
        Account = get_user_model()
        subscribed_to = Account.objects.get(username=creator_username)
        subscriber = request.user

        if Subscription.objects.filter(
            subscribed_to = subscribed_to,
            subscriber = subscriber
        ).exists():
            return Response("Subscription already exists.", status.HTTP_400_BAD_REQUEST)
        
        Subscription.objects.create(subscribed_to=subscribed_to, subscriber=subscriber)
        return Response("Subscription created.", status.HTTP_201_CREATED)

    def delete(self, request, creator_username, *args, **kwargs):
        Account = get_user_model()
        subscribed_to = Account.objects.get(username=creator_username)
        subscriber = request.user
        
        if not Subscription.objects.filter(
            subscribed_to = subscribed_to,
            subscriber = subscriber
        ).exists():
            return Response("Subscription does not exist.", status.HTTP_400_BAD_REQUEST)

        Subscription.objects.get(subscribed_to=subscribed_to, subscriber=subscriber).delete()
        return Response("Subscription deleted.", status.HTTP_204_NO_CONTENT)
