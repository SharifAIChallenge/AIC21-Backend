from django.shortcuts import render
from apps.gamedoc.serializers import *
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class GamedocAPIView(GenericAPIView):
    serializer_class = GamedocSerializer
    queryset = Gamedoc.objects.all()

    def get(self, request):
        gamedoc = self.get_serializer(self.get_queryset().last())
        return Response(data={"data": gamedoc.data}, status=status.HTTP_200_OK)
