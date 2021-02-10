from rest_framework.generics import GenericAPIView
from apps.rule.serializers import *
from rest_framework.response import Response

class RuleView(GenericAPIView):
    serializer_class = RuleSerializer
    queryset = Rule.objects.all().order_by('order')

    def get(self, request):
        rules = RuleSerializer(self.get_queryset(), many=True)
        return Response(rules.data)