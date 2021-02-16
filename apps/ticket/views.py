from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from apps.core.utils import send_to_telegram

from .models import Ticket
from .serializers import TicketSerializer
from .services import SendTicketToTelegramChannel


class TicketAPIView(GenericAPIView):
    serializer_class = TicketSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()

        send_to_telegram(serializer.data)

        return Response(
            data={'data': ticket},
            status=status.HTTP_201_CREATED
        )

    def get(self, request, token_id):
        ticket = get_object_or_404(Ticket, id=token_id)
        data = self.get_serializer(instance=ticket).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class UserTicketsListAPIView(GenericAPIView):
    serializer_class = TicketSerializer

    def get(self, request):
        tickets = Ticket.objects.filter(author=request.user)
        data = self.get_serializer(instance=tickets, many=True)

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class PublicTicketsListAPIView(GenericAPIView):
    serializer_class = TicketSerializer

    def get(self, request):
        tickets = Ticket.objects.filter(is_public=True)
        data = self.get_serializer(instance=tickets, many=True)

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )
