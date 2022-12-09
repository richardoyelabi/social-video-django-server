from django.urls import path
from media.views import MediaUploadView

urlpatterns = [
    path("", MediaUploadView.as_view(), name="media_upload"),
]