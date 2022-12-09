from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from media.models import Photo, Video
from media.serializers import PhotoSerializer, VideoSerializer


class MediaUploadView(APIView):
    """Upload a photo or video. 
    Accepts POST"""

    def post(self, request, *args, **kwargs):
        media_type = self.request.data.get("media_type")

        uploader = request.user.public_id
        media = request.data.get("media")

        data = {
            "uploader": uploader,
            "media": media
        }

        if media_type=="photo":
            serializer = PhotoSerializer(data=data)

        elif media_type=="video":
            serializer = VideoSerializer(data=data)

        else:
            return Response("Invalid media_type parameter", status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            new_media = serializer.save()

            public_id = new_media.public_id

            return Response({
                "public_id": public_id,
                "media_type": media_type
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    