from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import IdUpload
from .serializers import IdUploadSerializer
from .permissions import IsUnVerifiedCreator


class IdUploadView(CreateAPIView):
    """Upload id verification files.
    Accepts POST"""

    serializer_class = IdUploadSerializer
    queryset = IdUpload.objects.all()
    permission_classes = [IsUnVerifiedCreator]

    def post(self, request, *args, **kwargs):
        creator = request.user.id
        type = request.data.get("type")
        upload = request.data.get("upload")

        data = {"creator": creator, "type": type, "upload": upload}

        serializer = self.get_serializer_class()
        serializer = serializer(data=data)

        if serializer.is_valid():
            id_upload = serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
