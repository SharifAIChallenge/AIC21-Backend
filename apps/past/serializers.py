from rest_framework import serializers
from django.conf import settings
from apps.past.models import *

class PastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Past
        fields = ['id', 'title_en', 'title_fa', 'description_en',
                  'description_fa', 'firstTeam', 'secondTeam',
                  'thirdTeam', 'image']
