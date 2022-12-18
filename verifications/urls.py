from django.urls import path
from .views import IdUploadView

urlpatterns = [
    path("id-upload/", IdUploadView.as_view(), name="id_upload"),
]