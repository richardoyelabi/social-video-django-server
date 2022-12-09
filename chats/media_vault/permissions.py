from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    """Only creators have access"""

    def has_permission(self, request, view):
        if request.user.is_creator==True:
            if request.user.creatorinfo.is_verified==True:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(self, request, view)