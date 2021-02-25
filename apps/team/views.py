from django.shortcuts import render
from rest_framework import status, parsers
from rest_framework.generics import GenericAPIView, get_object_or_404

from apps.team.models import Submission
from apps.team.serializer import SubmissionSerializer, SubmissionPostSerializer
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _


class SubmissionsListAPIView(GenericAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get(self, request):
        if not hasattr(request.user, 'team'):
            return Response(data={'errors': ['Sorry! you dont have a team']},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        data = self.get_serializer(
            self.get_queryset().filter(team=request.user.team),
            many=True).data
        return Response(data={'submissions': data}, status=status.HTTP_200_OK)


class ChangeFinalSubmissionAPIView(GenericAPIView):

    def put(self, request, submission_id):
        if not hasattr(request.user, 'team'):
            return Response(data={'errors': ['Sorry! you dont have a team']},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        submission = get_object_or_404(Submission, id=submission_id)
        try:
            submission.set_final()
            return Response(
                data={'details': 'Final submission changed successfully'},
                status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(data={'errors': [str(e)]},
                            status=status.HTTP_406_NOT_ACCEPTABLE)


class SubmissionSubmitAPIView(GenericAPIView):
    serializer_class = SubmissionPostSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def post(self, request):
        submission = self.get_serializer(data=request.data,
                                         context={'request': request})
        if submission.is_valid(raise_exception=True):
            submission = submission.save()
            return Response(
                data={'details': _(
                    'Submission information successfully submitted'),
                    'submission_id': submission.id},
                status=status.HTTP_200_OK)
        return Response(data={'errors': [_('Something Went Wrong')]},
                        status=status.HTTP_406_NOT_ACCEPTABLE)