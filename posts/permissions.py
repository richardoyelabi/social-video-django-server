from rest_framework.permissions import BasePermission, SAFE_METHODS

class CommentOwnerOrReadOnly(BasePermission):
    """Give write access to an existing comment only to the owner of the account"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.account == request.user

class PostOwnerOrReadOnly(BasePermission):
    """Give write access to an existing post only to the owner of the account"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.uploader == request.user