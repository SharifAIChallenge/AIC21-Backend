from django.urls import path

from apps.notification.views import NotificationView, SubscriberView, \
    PublicNotificationsAPIView

urlpatterns = [
    path('', NotificationView.as_view(), name='notifications_list'),
    path('public', PublicNotificationsAPIView.as_view(),
         name='public_notifications_list'),
]
