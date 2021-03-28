from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('request', view=views.PaymentRequestAPIView.as_view(),
         name='payment_request'),
    path('callback', view=views.PaymentVerifyAPIView.as_view(),
         name='payment_callback'),
    path('config', view=views.PaymentConfigAPIView.as_view(),
         name='payment_config')
]
