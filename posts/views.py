from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView, DestroyAPIView, RetrieveDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import OrderingFilter
from posts.permissions import CommentOwnerOrReadOnly, PostOwnerOrReadOnly

from posts.models import Post, Like, Comment
from posts.serializers import PhotoPostCreateSerializer, VideoPostCreateSerializer, PhotoPostDetailSerializer, VideoPostDetailSerializer, LikeSerializer, CommentSerializer, CommentCreateSerializer

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

        return Response(likes_number)

    def post(self, request, post_id, *args, **kwargs):
        account = request.user
        post = Post.objects.get(public_id=post_id)

        if Like.objects.filter(
            account = account,
            post = post
        ).exists():
            return Response("User already liked this post.", status.HTTP_400_BAD_REQUEST)

        Like.objects.create(account=account, post=post)
        return Response("Post liked.", status.HTTP_201_CREATED)

    def delete(self, request, post_id, *args, **kwargs):
        account = request.user
        post = Post.objects.get(public_id=post_id)

        if not Like.objects.filter(
            account = account,
            post = post
        ).exists():
            return Response("Like relation does not exist.", status.HTTP_400_BAD_REQUEST)

        Like.objects.get(account=account, post=post).delete()
        return Response("Post unliked.", status.HTTP_204_NO_CONTENT)

class PostCommentView(ListModelMixin,GenericAPIView):
    """View comments or get the number of comments on a post.
    GET to retrieve the number of comments, 'list=True' to view comments; 
    POST to comment (comment_text)"""

    serializer_class = CommentSerializer
    lookup_field = "public_id"
    lookup_url_kwarg = "post_id"
    filter_backends = [OrderingFilter]
    ordering = ["time"]

    def get_queryset(self):
        return Comment.objects.filter(post__public_id=self.kwargs["post_id"])

    def get(self, request, post_id, *args, **kwargs):
        if request.query_params.get("list"):
            return self.list(request, *args, **kwargs)
            
        post = Post.objects.get(public_id=post_id)
        comments_number = post.comments_number
        return Response(comments_number)

class CommentCreateView(GenericAPIView):
    """Create new comment.
    Accepts POST"""

    serializer_class = CommentCreateSerializer
    lookup_field = "public_id"
    lookup_url_kwarg = "post_id"

    def post(self, request, post_id, *args, **kwargs):
        account = request.user.public_id
        comment_text = request.POST.get("comment_text")

        data = {"account":account, "comment_text":comment_text, "post":post_id}
        serializer = CommentCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class CommentView(DestroyAPIView):
    """Delete comment.
    Accepts DELETE"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "public_id"
    lookup_url_kwarg = "comment_id"
    permission_classes = [CommentOwnerOrReadOnly]

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
        
        if post_type=="photo":
            return PhotoPostDetailSerializer
        return VideoPostDetailSerializer

class CreatePostView(CreateAPIView):
    """Create a new post.
    Accepts POST"""

    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        post_type = self.request.data.get("post_type")

        if post_type=="photo":
            return PhotoPostCreateSerializer
        return VideoPostCreateSerializer

    def post(self, request, *args, **kwargs):
        post_type = self.request.data.get("post_type")

        uploader_public_id = request.user.public_id
        media = request.data.get("media_item.media")
        caption = request.data.get("caption")

        data = {
            "post_type": post_type, 
            "uploader": uploader_public_id,
            "media_item": {
                "uploader": uploader_public_id,
                "content_type": "", 
                "media": media
            }, 
            "caption":caption
        }
        
        #Set serialization process based on post_type
        if post_type=="photo":
            data["media_item"]["content_type"] = "post"
            serializer = PhotoPostCreateSerializer(data=data)
        else:
            if post_type=="free_video":
                data["media_item"]["content_type"] = "free_post"
            elif post_type=="paid_video":
                data["media_item"]["content_type"] = "paid_post"
            else:
                return Response("Invalid post_type parameter", status=status.HTTP_400_BAD_REQUEST)
            serializer = VideoPostCreateSerializer(data=data)

        if serializer.is_valid():
            new_post = serializer.save()

            if post_type=="photo":
                serializer = PhotoPostDetailSerializer(new_post)
            else:
                serializer = VideoPostDetailSerializer(new_post)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
