from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from apps.core.utils import send_to_telegram

from apps.ticket import paginations
from .models import Ticket, Reply
from .serializers import TicketSerializer, ReplySerializer
from .services import SendTicketToTelegramChannel


class TicketAPIView(GenericAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        data = self.get_serializer(instance=ticket).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def put(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        serializer = self.get_serializer(instance=ticket, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"detail": "Your change has been submitted"},
            status=status.HTTP_200_OK
        )


class UserTicketsListAPIView(GenericAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()

        # send_to_telegram(serializer.data)

        return Response(
            data={"detail": "Your ticket has been submitted"},
            status=status.HTTP_201_CREATED
        )

    def get(self, request):
        tickets = Ticket.objects.filter(author=request.user)
        data = self.get_serializer(instance=tickets, many=True).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class PublicTicketsListAPIView(GenericAPIView):
    serializer_class = TicketSerializer

    def get(self, request):
        tickets = Ticket.objects.filter(is_public=True)
        data = self.get_serializer(instance=tickets, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class ReplyListAPIView(GenericAPIView):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all().order_by('-created')
    pagination_class = paginations.ReplyPagination
    permission_classes = [IsAuthenticated,]

    def get(self, request, ticket_id):
        replies = self.get_queryset().filter(ticket__id=ticket_id)
        data = ReplySerializer(replies, many=True).data
        return Response(data)

    def post(self, request, ticket_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Your Reply has been submitted"})

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['ticket_id'] = self.kwargs.get('ticket_id')

        return ctx


class ReplyAPIView(GenericAPIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, ticket_id, reply_id):
        reply = get_object_or_404(Reply, id=reply_id)
        data = self.get_serializer(instance=reply).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def put(self, request, ticket_id, reply_id):
        reply = get_object_or_404(Reply, id=reply_id)
        serializer = self.get_serializer(instance=reply, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"detail": "Your change has been submitted"},
            status=status.HTTP_200_OK
        )
