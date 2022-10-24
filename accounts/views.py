from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Account
from accounts.serializers import UserPublicProfileSerializer, UserPrivateProfileSerializer, CreatorPublicProfileSerializer, CreatorPrivateProfileSerializer

class ProfileView(APIView):
    """Profile information for user whose username the url points to.
    Accepts GET and POST.
    """

    def get_object(self, username):
        """Get the account object corresponding to parameter from url"""
        try:
            return Account.objects.get(username=username)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):

        def get_serializer(account):
            """Choose the appropriate serializer according to privacy and user type (creator or not)"""
            is_owner = request.user.id ==account.id
            is_creator = account.is_creator

            if is_owner:
                if is_creator:
                    return CreatorPrivateProfileSerializer(account)
                else:
                    return UserPrivateProfileSerializer(account)
            else:
                if is_creator:
                    return CreatorPublicProfileSerializer(account)
                else:
                    return UserPublicProfileSerializer(account)

        account = self.get_object(username)
        serializer = get_serializer(account)
        return Response(serializer.data)

    def post(self, request, username, format=None):
        
        def get_serializer(account):
            """Choose the appropriate serializer according to privacy and user_type (creator or not)"""
            is_owner = request.user.id ==account.id
            is_creator = account.is_creator

            if is_owner:
                if is_creator:
                    return CreatorPrivateProfileSerializer(account)
                else:
                    return UserPrivateProfileSerializer(account)
            else:
                return status.HTTP_403_FORBIDDEN

        account = self.get_object(username)
        serializer = get_serializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        