from django.urls import path
from video_purchases.views import PurchaseView

urlpatterns = [
    path("<uuid:video_id>/", PurchaseView.as_view(), name="purchase-video")
]