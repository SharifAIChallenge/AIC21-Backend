from django.urls import path
from apps.ticket.views import PublicTicketsListAPIView, TicketAPIView, UserTicketsListAPIView,ReplyListAPIView

urlpatterns = [
    path('', UserTicketsListAPIView.as_view()),
    path('publicTickets', PublicTicketsListAPIView.as_view()),
    path('<str:ticket_id>', TicketAPIView.as_view()),
    path('<str:ticket_id>/replies', ReplyListAPIView.as_view()),

]