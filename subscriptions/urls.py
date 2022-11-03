from django.urls import path
from subscriptions.views import SubscriptionView

urlpatterns = [
    path("<creator_id>/", SubscriptionView.as_view(), name="subscription")
]