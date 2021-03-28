from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.ticket.models import Ticket, TicketStatus
from apps.ticket.serializers import TicketSerializer, LimitedTicketSerializer


class TicketAPIView(GenericAPIView):
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    queryset = Ticket.objects.all()

    def get(self, request):
        data = LimitedTicketSerializer(
            instance=self.get_queryset(),
            many=True
        ).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def put(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)

        ticket.is_public = not ticket.is_public

        ticket.save()

        return Response(
            status=status.HTTP_200_OK
        )

    def delete(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)

        ticket.status = TicketStatus.CLOSED
        ticket.save()

        return Response(
            status=status.HTTP_200_OK
        )
