from rest_framework.generics import GenericAPIView
from apps.rule.serializers import *
from rest_framework import status
from rest_framework.response import Response

class RuleAPIView(GenericAPIView):
    serializer_class = RuleSerializer
    queryset = Rule.objects.all().order_by('order')

    def get(self, request):
        rules = self.get_serializer(self.get_queryset(), many=True)
        return Response(data={"data": rules.data}, status=status.HTTP_200_OK)