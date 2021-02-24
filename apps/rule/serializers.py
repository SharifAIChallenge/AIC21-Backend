from rest_framework import serializers
from apps.rule.models import Rule

class RuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rule
        fields = ['title_en', 'title_fa', 'text_en', 'text_fa', 'order']