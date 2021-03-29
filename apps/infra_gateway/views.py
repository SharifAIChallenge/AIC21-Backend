from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from apps.challenge.models import Match
from apps.infra_gateway.permissions import IsInfra
from apps.infra_gateway.serializers import InfraEventPushSerializer
from apps.team.models import Submission

from .serializers import InfraEventPush


class InfraEventPushAPIView(GenericAPIView):
    serializer_class = InfraEventPushSerializer
    permission_classes = (IsInfra,)

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        event = serializer.save()

        return Response(
            data={
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
