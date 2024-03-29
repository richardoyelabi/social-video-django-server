from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import WithdrawalRequest
from .permissions import IsCreator


class WithdrawView(APIView):
    """Send a request for payment. Valid only for creators.
    Accepts POST."""

    permission_classes = [IsCreator]

    def post(self, request, *args, **kwargs):
        creator = request.user

        try:
            WithdrawalRequest.objects.create(creator=creator)

        except:
            return Response(
                "Something went wrong", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response("Request for withdrawal sent", status=status.HTTP_202_ACCEPTED)
