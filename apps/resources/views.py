from django.shortcuts import render

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import ProfileComplete


from .serializers import ResourceSerializer, DownloadLinkSerializer
from .models import Resource, DownloadLink


# Create your views here.

class ResourceAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, ProfileComplete)
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'data':data})
