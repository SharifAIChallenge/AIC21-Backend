from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from apps.infra_gateway.permissions import IsInfra
from apps.infra_gateway.serializers import CompiledSubmissionSerializer
from apps.team.models import Submission


class UpdateSubmissionAPIView(GenericAPIView):
    queryset = Submission.objects.all()
    serializer_class = CompiledSubmissionSerializer
    permission_classes = (IsInfra,)

    def put(self, request, submission_id):
        submission = get_object_or_404(Submission, id=submission_id)
        submission = self.get_serializer(data=request.data,
                                   instance=submission)
        submission.is_valid(raise_exception=True)
        submission.save()

        return Response(
            data={
                "data": submission.data
            },
            status=status.HTTP_200_OK
        )

