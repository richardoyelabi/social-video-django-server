from django.urls import path
from tips.views import TipView

urlpatterns = [
    path("<uuid:creator_id>/", TipView.as_view(), name="tip")
]