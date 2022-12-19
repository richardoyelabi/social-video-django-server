from django.urls import path
from subscriptions.views import SubscriptionView, SetSubscriptionView

urlpatterns = [
    path("set-fee/", SetSubscriptionView.as_view(), name="set_subscription_fee"),
    path("<creator_id>/", SubscriptionView.as_view(), name="subscription"),
]