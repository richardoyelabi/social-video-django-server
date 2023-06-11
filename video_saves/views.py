from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from video_saves.models import VideoSave
from posts.models import Post
from video_saves.serializers import VideoSaveSerializer


class VideoSaveView(GenericAPIView):
    """Save or 'unsave' a video.
    Accepts POST and DELETE."""

    queryset = VideoSave.objects.all()
    serializer_class = VideoSaveSerializer
    lookup_url_kwarg = "post_id"

    def post(self, request, post_id, *args, **kwargs):
        account = request.user
        post = Post.objects.get(public_id=post_id)

        if VideoSave.objects.filter(account=account, video_post=post).exists():
            return Response(
                "User already saved this video.", status.HTTP_400_BAD_REQUEST
            )

        VideoSave.objects.create(account=account, video_post=post)
        return Response("Video saved.", status.HTTP_201_CREATED)

    def delete(self, request, post_id, *args, **kwargs):
        account = request.user
        post = Post.objects.get(public_id=post_id)

        if not VideoSave.objects.filter(account=account, video_post=post).exists():
            return Response("User never saved this video.", status.HTTP_400_BAD_REQUEST)

        VideoSave.objects.get(account=account, video_post=post).delete()
        return Response("Video save undone.", status.HTTP_204_NO_CONTENT)
