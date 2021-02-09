from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins

from apps.past.serializers import PastSerializer
from apps.past.models import Past


class PastView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin):

    queryset = Past.objects.all()
    serializer_class = PastSerializer