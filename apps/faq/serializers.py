from rest_framework.serializers import ModelSerializer

from .models import QuestionTitle, QuestionWithAnswer


class QuestionWithAnswerSerializer(ModelSerializer):
    class Meta:
        model = QuestionWithAnswer
        exclude = ['id']


class QuestionTitleSerializer(ModelSerializer):
    faqs = QuestionWithAnswerSerializer(read_only=True, many=True)

    class Meta:
        model = QuestionTitle
        fields = ('title', 'faqs')
