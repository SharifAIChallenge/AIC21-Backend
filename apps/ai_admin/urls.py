from django.urls import path

from . import views

app_name = 'ai_admin'

urlpatterns = [
    path('ticket', view=views.TicketAPIView.as_view(), name='ticket_admin'),
]
