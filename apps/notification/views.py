from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from .models import Notification, Subscriber
from .serializers import (NotificationSerializer, SubscriberSerializer,
                          PublicNotificationSerializer)


class NotificationView(GenericAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        notifications = request.user.notifications.all()
        data = self.get_serializer(notifications, many=True).data
        return Response(data={'notifications': data},
                        status=status.HTTP_200_OK)

    def post(self, request):
        request.user.notifications.all().update(seen=True)

        return Response(status=status.HTTP_200_OK)


class PublicNotificationsAPIView(GenericAPIView):
    queryset = Notification.objects.all()
    serializer_class = PublicNotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        notifications = self.get_queryset().filter(for_all=True)
        data = self.get_serializer(notifications, many=True).data
        return Response(data={'notifications': data},
                        status=status.HTTP_200_OK)


class SubscriberView(GenericAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    def post(self, request):
        subscriber = self.get_serializer(data=request.data)
        if subscriber.is_valid():
            subscriber.save()
            return Response(subscriber.data)
        return Response({'detail': 'something is wrong'})
