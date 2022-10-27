from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from accounts.models import Account
from accounts.serializers import UserPublicProfileSerializer, UserPrivateProfileSerializer,\
    CreatorPublicProfileSerializer, CreatorPrivateProfileSerializer
from accounts.permissions import OwnerOrReadOnly

class ProfileView(RetrieveUpdateAPIView):
    """Profile information for user whose username the url points to.
    Accepts GET, PUT and PATCH.
    Weird Note: Even with PUT, "profile_photo" and "cover_photo" can be left blank without deleting existing value in database.\
        This is to prevent unnecessary image file overhead in every PUT request.
    """
    queryset = Account.objects.all()
    lookup_field = "public_id"
    lookup_url_kwarg = "id"
    permission_classes = [OwnerOrReadOnly]

    def get_serializer_class(self):
        """Choose the appropriate serializer according to privacy and user type (creator or not)"""

        account = self.get_object()
        is_owner = self.request.user.id == account.id
        is_creator = account.is_creator

        if is_owner:
            if is_creator:
                return CreatorPrivateProfileSerializer
            else:
                return UserPrivateProfileSerializer
        else:
            if is_creator:
                return CreatorPublicProfileSerializer
            else:
                return UserPublicProfileSerializer

class MyProfileURLView(APIView):
    """Return profile url of authenticated user.
    Accepts GET."""

    def get(self, request):
        public_id = request.user.public_id
        url = reverse("profile", args=[public_id], request=request)
        return Response({"profile_url": url})
