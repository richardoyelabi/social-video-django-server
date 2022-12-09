from django.urls import path
from .views import ChatVaultView, ChatVaultVideoStream


urlpatterns = [
    path("", ChatVaultView.as_view(), name="chat_media_vault"),
    path("video-stream/<uuid:video_id>/", ChatVaultVideoStream.as_view(), name="vault_video_preview"),
]