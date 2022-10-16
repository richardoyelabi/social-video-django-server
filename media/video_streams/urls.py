from django.urls import path

from media.video_streams.views import VideoStreamAPIRedirectView

urlpatterns = [
    path("", VideoStreamAPIRedirectView.as_view(), name="video-stream")
]
