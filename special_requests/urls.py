from django.urls import path
from special_requests.views import MessagePurchaseView

urlpatterns = [
    path("<uuid:message_id>/", MessagePurchaseView.as_view(), name="special-request")
]
