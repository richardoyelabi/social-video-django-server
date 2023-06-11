from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from video_purchases.models import Purchase
from video_purchases.serializers import PurchaseSerializer
from posts.models import Post
from transactions.exceptions import TransactionInsufficientBalanceError


class PurchaseView(GenericAPIView):
    """Purchase a post video.
    Accepts POST."""

    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    lookup_url_kwarg = "post_id"

    def post(self, request, post_id, *args, **kwargs):
        buyer = request.user
        post = Post.objects.get(public_id=post_id)

        if post.post_type != "paid_video":
            return Response(
                "Media doesn't require purchase", status.HTTP_400_BAD_REQUEST
            )

        if Purchase.objects.filter(buyer=buyer, video_post=post).exists():
            return Response(
                "User already purchased the video.", status.HTTP_400_BAD_REQUEST
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
            Purchase.objects.create(buyer=buyer, video_post=post, fee_currency=currency)
        except TransactionInsufficientBalanceError as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)

        return Response("Video purchased.", status.HTTP_201_CREATED)
