from rest_framework.permissions import BasePermission


class IsUnVerifiedCreator(BasePermission):
    """Authorize only unverified creators"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_creator and not request.user.creatorinfo.is_verified:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(self, request, view)