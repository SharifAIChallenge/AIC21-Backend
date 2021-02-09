from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.past.serializers import *

# Create your views here.

class PastView(GenericAPIView):
    serializer_class = PastSerializer
    queryset = Past.objects.all().order_by('-date')

    def get(self, request):
        past = PastSerializer(self.get_queryset(), many=True)
        return Response(past.data)