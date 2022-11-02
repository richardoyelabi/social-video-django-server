from django.urls import path
from video_purchases.views import PurchaseView

urlpatterns = [
    path("<uuid:post_id>/", PurchaseView.as_view(), name="purchase-video")
]