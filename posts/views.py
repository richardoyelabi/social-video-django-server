from rest_framework.mixins import ListModelMixin
from rest_framework.generics import (
    GenericAPIView,
    DestroyAPIView,
    RetrieveDestroyAPIView,
    CreateAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from posts.permissions import CommentOwnerOrReadOnly, PostOwnerOrReadOnly
from posts.models import Post, Like, Comment, View
from posts.serializers import (
    BasePostCreateSerializer,
    PhotoPostCreateSerializer,
    VideoPostCreateSerializer,
    PaidVideoPostCreateSerializer,
    PhotoPostDetailSerializer,
    VideoPostDetailSerializer,
    PaidVideoPostDetailSerializer,
    ViewSerializer,
    LikeSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)
from sage_stream.api.views import VideoStreamAPIView, PreviewStreamAPIView
from utils.paginations import CustomCursorPagination
from media.models import Video
from subscriptions.models import Subscription


class PostViewView(GenericAPIView):
    """Send acknowledgement that post made an impression on user.
    Accepts POST."""

    serializer_class = ViewSerializer
    lookup_field = "public_id"
    lookup_url_kwarg = "post_id"

    def post(self, request, post_id, *args, **kwargs):
        account = request.user
        post = Post.objects.get(public_id=post_id)

        View.objects.create(account=account, post=post)

        return Response("Post view acknowledged", status.HTTP_202_ACCEPTED)


class PostLikeView(GenericAPIView):
    """Like, unlike, or get the number of likes of a post.
    GET to retrieve the number of likes; POST to like; DELETE to unlike."""

    serializer_class = LikeSerializer
    lookup_field = "public_id"
    lookup_url_kwarg = "post_id"

    def get_queryset(self):
        return Like.objects.filter(post__public_id=self.kwargs["post_id"])

    def get(self, request, post_id, *args, **kwargs):
        post = Post.objects.get(public_id=post_id)
        likes_number = post.likes_number

        return Response({"like_count": likes_number})

    def post(self, request, post_id, *args, **kwargs):
        account = request.user
        post = Post.objects.get(public_id=post_id)

        if Like.objects.filter(account=account, post=post).exists():
            return Response(
                "User already liked this post.", status.HTTP_400_BAD_REQUEST
            )

        Like.objects.create(account=account, post=post)

        self.send_like_count_update(post)

        return Response("Post liked.", status.HTTP_201_CREATED)

    def delete(self, request, post_id, *args, **kwargs):
        account = request.user
        post = Post.objects.get(public_id=post_id)

        if not Like.objects.filter(account=account, post=post).exists():
            return Response(
                "Like relation does not exist.", status.HTTP_400_BAD_REQUEST
            )

        Like.objects.get(account=account, post=post).delete()

        self.send_like_count_update(post)

        return Response("Post unliked.", status.HTTP_204_NO_CONTENT)

    def send_like_count_update(self, post):
        """Send updated number of likes to consumers listening to like_count_..."""

        post.refresh_from_db(fields=["likes_number"])

        likes_number = post.likes_number
        post_id = post.public_id

        async_to_sync(get_channel_layer().group_send)(
            f"like_count_{post_id}",
            {"type": "like_count_update", "content": {"like_count": likes_number}},
        )


class PostCommentView(ListModelMixin, GenericAPIView):
    """View comments.
    Accepts GET"""

    serializer_class = CommentSerializer
    lookup_field = "public_id"
    lookup_url_kwarg = "post_id"

    class Pagination(CustomCursorPagination):
        ordering = "time"

    pagination_class = Pagination

    def get_queryset(self):
        return Comment.objects.filter(post__public_id=self.kwargs["post_id"])

    def get(self, request, post_id, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CommentCreateView(GenericAPIView):
    """Create new comment.
    Accepts POST"""

    serializer_class = CommentCreateSerializer
    lookup_field = "public_id"
    lookup_url_kwarg = "post_id"

    def post(self, request, post_id, *args, **kwargs):
        account = request.user.public_id
        comment_text = request.POST.get("comment_text")

        data = {"account": account, "comment_text": comment_text, "post": post_id}

        serializer = CommentCreateSerializer(data=data)

        if serializer.is_valid():
            comment = serializer.save()
            comment_data = CommentSerializer(comment).data
            comment_data["post"] = str(comment_data["post"])

            post = Post.objects.get(public_id=post_id)

            self.send_new_comment(post, comment_data)

            self.send_comment_count(post)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_comment_count(self, post):
        """Send updated number of comments to consumers listening to comment_count_..."""

        post.refresh_from_db(fields=["comments_number"])

        comments_number = post.comments_number
        post_id = post.public_id

        async_to_sync(get_channel_layer().group_send)(
            f"comment_count_{post_id}",
            {
                "type": "comment_count_update",
                "content": {"comment_count": comments_number},
            },
        )

    def send_new_comment(self, post, comment_data):
        """Send new comment to consumers listening for new comment"""

        post_id = post.public_id

        async_to_sync(get_channel_layer().group_send)(
            f"comments_{post_id}",
            {
                "type": "comment_update",
                "content": {"type": "create", "data": comment_data},
            },
        )


class CommentView(DestroyAPIView):
    """Delete comment.
    Accepts DELETE"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "public_id"
    lookup_url_kwarg = "comment_id"
    permission_classes = [CommentOwnerOrReadOnly]

    def destroy(self, request, comment_id, *args, **kwargs):
        try:
            comment = Comment.objects.get(public_id=comment_id)

        except Comment.DoesNotExist:
            return Response("Comment does not exist.", status.HTTP_400_BAD_REQUEST)

        comment.delete()

        self.send_comment_delete(comment.post, comment)
        self.send_comment_count(comment.post)

        return Response("Comment deleted.", status.HTTP_204_NO_CONTENT)

    def send_comment_count(self, post):
        """Send updated number of comments to consumers listening to comment_count_..."""

        post.refresh_from_db(fields=["comments_number"])

        comments_number = post.comments_number
        post_id = post.public_id

        async_to_sync(get_channel_layer().group_send)(
            f"comment_count_{post_id}",
            {
                "type": "comment_count_update",
                "content": {"comment_count": comments_number},
            },
        )

    def send_comment_delete(self, post, comment):
        """Notify PostCommentsConsumer if a comment is deleted"""

        post_id = post.public_id
        comment_id = str(comment.public_id)

        async_to_sync(get_channel_layer().group_send)(
            f"comments_{post_id}",
            {
                "type": "comment_update",
                "content": {"type": "delete", "data": comment_id},
            },
        )


class PostView(RetrieveDestroyAPIView):
    """View or delete post.
    Accepts GET and DELETE"""

    queryset = Post.objects.all()
    lookup_field = "public_id"
    lookup_url_kwarg = "post_id"
    permission_classes = [PostOwnerOrReadOnly]

    def get_serializer_class(self):
        post = Post.objects.get(public_id=self.kwargs["post_id"])
        post_type = post.post_type

        if post_type == "photo":
            return PhotoPostDetailSerializer
        elif post_type == "free_video":
            return VideoPostDetailSerializer
        elif post_type == "paid_video":
            return PaidVideoPostDetailSerializer


class CreatePostView(CreateAPIView):
    """Create a new post.
    Accepts POST with parameters post_type, media, caption,
    purchase_cost_currency and purchase_cost_amount"""

    queryset = Post.objects.all()
    serializer_class = BasePostCreateSerializer

    def post(self, request, *args, **kwargs):
        post_type = self.request.data.get("post_type")

        uploader_public_id = request.user.public_id
        media = request.data.get("media")
        caption = request.data.get("caption")

        data = {
            "post_type": post_type,
            "uploader": uploader_public_id,
            "media_item": {"uploader": uploader_public_id, "media": media},
            "caption": caption,
        }

        # Set serialization process based on post_type

        if post_type == "photo":
            serializer = PhotoPostCreateSerializer(data=data)

        else:
            if post_type == "free_video":
                serializer = VideoPostCreateSerializer(data=data)

            elif post_type == "paid_video":
                (
                    data["purchase_cost_currency"],
                    data["purchase_cost_amount"],
                ) = request.data.get("purchase_cost_currency"), request.data.get(
                    "purchase_cost_amount"
                )

                serializer = PaidVideoPostCreateSerializer(data=data)

            else:
                return Response(
                    "Invalid post_type parameter", status=status.HTTP_400_BAD_REQUEST
                )

        if serializer.is_valid():
            new_post = serializer.save()

            if post_type == "photo":
                serializer = PhotoPostDetailSerializer(new_post)
            elif post_type == "free_video":
                serializer = VideoPostDetailSerializer(new_post)
            elif post_type == "paid_video":
                serializer = PaidVideoPostDetailSerializer(new_post)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostVideoStreamView(VideoStreamAPIView):
    """Stream post video.
    Accepts GET"""

    def get(self, request, post_id, video_id, *args, **kwargs):
        """Authorize user to view stream and call super() to send stream"""

        post = Post.objects.get(public_id=post_id)
        video = Video.objects.get(public_id=video_id)

        error_response = Response(
            "You're not authorized to watch this video. Please purchase video or subscribe to creator to unlock.",
            status=status.HTTP_401_UNAUTHORIZED,
        )

        if post.media_item != video:
            return error_response

        user = request.user
        post_creator = post.uploader

        if (
            post.post_type == "free_video"
            or Subscription.objects.filter(
                subscribed_to=post_creator, subscriber=user
            ).exists()
            or post.buyers.filter(id=user.id).exists()
            or user == post_creator
        ):
            return super().get(request, video_id)

        return error_response


class PreviewVideoStreamView(PreviewStreamAPIView):
    """Stream previews premium video posts.
    Accepts GET"""

    def get(self, request, post_id, *args, **kwargs):
        return super().get(request, post_id, *args, **kwargs)
