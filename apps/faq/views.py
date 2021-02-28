from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import QuestionTitleSerializer
from .models import QuestionTitle


# Create your views here.

class FaqsAPIView(GenericAPIView):
    queryset = QuestionTitle.objects.all()
    serializer_class = QuestionTitleSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'data': data}, status=status.HTTP_200_OK)
