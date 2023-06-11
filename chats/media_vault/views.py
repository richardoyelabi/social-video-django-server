from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from .permissions import IsCreator
from utils.paginations import CustomCursorPagination
from media.models import Photo, Video, Media
from .serializers import VaultSerializer
from sage_stream.api.views import VideoStreamAPIView


class ChatVaultView(ListAPIView):
    """
    View recent media used in chat messages.
    Accepts GET.
    ?type=photo to view photos, ?type=video to view videos, defaults to a mix of photos and videos
    """

    serializer_class = VaultSerializer
    pagination_class = CustomCursorPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ["-upload_time"]
    ordering = ordering_fields[0]
    permission_classes = [IsCreator]

    def get_queryset(self):
        creator = self.request.user
        media_type = self.request.query_params.get("type")

        if media_type == "photo":
            return Photo.objects.filter(uploader=creator).order_by("-upload_time")

        elif media_type == "video":
            return Video.objects.filter(uploader=creator).order_by("-upload_time")

        else:
            return Media.objects.filter(uploader=creator).order_by("-upload_time")


class ChatVaultVideoStream(VideoStreamAPIView):
    """Stream video in vault (for video creator only).
    Accepts GET"""

    def get(self, request, video_id, *args, **kwargs):
        """Authorize user to view stream and call super() to send stream"""

        video = Video.objects.get(public_id=video_id)

        error_response = Response(
            "You're not authorized to watch this video.",
            status=status.HTTP_403_FORBIDDEN,
        )

        user = request.user
        creator = video.uploader

        if user == creator:
            return super().get(request, video_id)

        return error_response
