from rest_framework.permissions import BasePermission, SAFE_METHODS

class OwnerOrReadOnly(BasePermission):
    """Give write access on an account only to the owner of the account"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.id == request.user.id