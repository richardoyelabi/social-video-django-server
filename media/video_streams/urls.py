from django.urls import path

from media.video_streams.views import VideoStreamAPIView

urlpatterns = [
    path("", VideoStreamAPIView.as_view(), name="video-stream")
]
