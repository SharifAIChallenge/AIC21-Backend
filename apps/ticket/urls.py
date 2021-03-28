from django.urls import path
from apps.ticket.views import PublicTicketsListAPIView, TicketAPIView, UserTicketsListAPIView, ReplyListAPIView, \
    ReplyAPIView, TagAPIView

urlpatterns = [
    path('', UserTicketsListAPIView.as_view()),
    path('publicTickets', PublicTicketsListAPIView.as_view()),
    path('tags', TagAPIView.as_view()),
    path('<str:ticket_id>', TicketAPIView.as_view()),
    path('<str:ticket_id>/replies', ReplyListAPIView.as_view()),
    path('<str:ticket_id>/replies/<str:reply_id>',ReplyAPIView.as_view()),
]
