from django.urls import path
from apps.ticket.views import PublicTicketsListAPIView, TicketAPIView, \
    UserTicketsListAPIView, ReplyListAPIView, \
    ReplyAPIView, TagAPIView, GhasemzadehAPIView

urlpatterns = [
    path('', UserTicketsListAPIView.as_view()),
    path('publicTickets', PublicTicketsListAPIView.as_view()),
    path('tags', TagAPIView.as_view()),
    path('db-balad-boodaneto-be-rokh-nakesh-aghaye-ghasemzadeh',
         view=GhasemzadehAPIView.as_view()),
    path('<str:ticket_id>', TicketAPIView.as_view()),
    path('<str:ticket_id>/replies', ReplyListAPIView.as_view()),
    path('<str:ticket_id>/replies/<str:reply_id>', ReplyAPIView.as_view()),
]
