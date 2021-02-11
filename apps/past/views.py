from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from apps.past.serializers import PastSerializer
from apps.past.models import Past
from django.shortcuts import get_object_or_404


class PastListAPIView(GenericAPIView):
    queryset = Past.objects.all()
    serializer_class = PastSerializer

    def get(self, request):
        pastAIs = self.get_serializer(self.get_queryset(), many=True)
        return Response(data={"data": pastAIs.data}, status=status.HTTP_200_OK)

class PastInstanceAPIView(GenericAPIView):
    
    def get(self, request, past_id):
        past_ai = get_object_or_404(Past.objects.all(), pk=past_id)
        data = PastSerializer(past_ai).data
        return Response(data={"data": data}, status=status.HTTP_200_OK)