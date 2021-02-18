from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import ResourceSerializer, DownloadLinkSerializer
from .models import Resource, DownloadLink
from rest_framework.response import Response


# Create your views here.

class ResourceAPIView(GenericAPIView):
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'data':data})
