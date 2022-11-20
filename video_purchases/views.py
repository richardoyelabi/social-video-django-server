from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from video_purchases.models import Purchase
from video_purchases.serializers import PurchaseSerializer
from posts.models import Post

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
            return Response("Media doesn't require purchase", status.HTTP_400_BAD_REQUEST)

        if Purchase.objects.filter(
            buyer = buyer,
            video_post = post
        ).exists():
            return Response("User already purchased the video.", status.HTTP_400_BAD_REQUEST)
        
        Purchase.objects.create(buyer=buyer, video_post=post)
        return Response("Video purchased.", status.HTTP_201_CREATED)
