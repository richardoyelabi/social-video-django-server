from rest_framework.permissions import BasePermission
from media.models import Video
from django.conf import settings

class HasSubscribedOrPurchasedVideo(BasePermission):
    """Custom permission class for VideoStreamAPIView"""

    def check_permission(self, request):
        user = request.user
        video_name = request.GET.get("path").replace(settings.MEDIA_URL, "")
        instance = Video.objects.get(video=video_name)
        content_type = instance.content_type

        if (content_type=="free_post" or content_type=="free_chat"):
            return True
        elif (content_type=="paid_post"):
            if (user.subscriptions.filter(id=instance.uploader.id).exists()): #If user is subscribed to video creator
                return True
            elif (instance.buyers.filter(id=user.id).exists()): #If user has purchased the video
                return True
            else:
                return False
        elif (content_type=="paid_chat"):
            if (instance.buyers.filter(id=user.id).exists()): #If user has purchased the video
                return True
        else:
            return False

    def has_permission(self, request, view):
        return self.check_permission(request)

    def has_object_permission(self, request, view, obj):
        return self.check_permission(request)
