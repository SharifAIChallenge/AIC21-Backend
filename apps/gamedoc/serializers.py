from rest_framework import serializers
from apps.gamedoc.models import Gamedoc


class GamedocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamedoc
        fields = ['link', 'title', 'repo_name', 'user_name']
