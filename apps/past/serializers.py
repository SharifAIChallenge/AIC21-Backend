from rest_framework import serializers
from django.conf import settings
from apps.past.models import *

class PastSerializer(serializers.ModelSerializer):

    num_comments = serializers.SerializerMethodField()

    class Meta:
        model = Past
        fields = ['title_en', 'title_fa', 'description_en',
                  'description_fa', 'firstTeam', 'secondTeam',
                  'thirdTeam']

    def get_num_comments(self, obj):
        return obj.comments.count()
