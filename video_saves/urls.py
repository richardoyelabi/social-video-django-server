from django.urls import path
from video_saves.views import VideoSaveView

urlpatterns = [
    path("<uuid:post_id>/", VideoSaveView.as_view(), name="save"),
]
