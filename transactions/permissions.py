from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    """Authorize only creators"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_creator:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(self, request, view)