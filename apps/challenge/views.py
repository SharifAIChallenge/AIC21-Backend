from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.team.permissions import HasTeam

from .models import Request, RequestTypes
from .serializers import RequestSerializer


class RequestAPIView(GenericAPIView):
    serializer_class = RequestSerializer
    permission_classes = (HasTeam,)
    queryset = Request.objects.all()

    def get(self, request):
        data = self.get_serializer(
            instance=self.get_queryset(),
            many=True
        ).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def put(self, request):
        pass

    def get_queryset(self):
        source = self.request.query_params.get(
            key='source',
            default=1
        )
        try:
            source = int(source)
        except ValueError:
            source = 1

        request_type = self.request.query_params.get(
            key='type',
            default=None
        )
        queryset = self.queryset

        queryset = (queryset.filter(source_team=self.request.user)
                    if source else
                    queryset.filter(target_team=self.request.user))

        queryset = (queryset.filter(type=request_type)
                    if request_type else
                    queryset)

        return queryset
