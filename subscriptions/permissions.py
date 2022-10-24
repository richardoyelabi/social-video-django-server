from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

class SubscriberIsUser(BasePermission):
    """Custom permission class for subscriptions views"""

    def check_permission(self, request):
        user = request.user
        subscriber = request.data.get("subscriber")
        if get_user_model().objects.get(username=subscriber)==user.username:
            return True
        return False

    def has_permission(self, request, view):
        return self.check_permission(request)

    def has_object_permission(self, request, view, obj):
        return self.check_permission(request)
