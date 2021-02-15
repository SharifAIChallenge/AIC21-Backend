from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .models import Ticket
from .serializers import TicketSerializer


class TicketAPIView(GenericAPIView):
    serializer_class = TicketSerializer
    lookup_field = 'pk'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()

        return Response(
            data={'data': ticket},
            status=status.HTTP_201_CREATED
        )

    def get(self, request, token_uuid):
        pass
