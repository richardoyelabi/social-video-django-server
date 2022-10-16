from rest_framework.views import APIView
from django.shortcuts import redirect

from .permissions import HasSubscribedOrPurchasedVideo

class VideoStreamAPIRedirectView(APIView):
    permission_classes = (HasSubscribedOrPurchasedVideo,)

    def get(self, request, *args, **kwargs):
        """Redirect request to sage_stream"""
        response = redirect(f"/video-api/?path={request.path}")
        return response