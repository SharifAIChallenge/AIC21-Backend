from rest_framework import serializers
from .models import Team


class TeamPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['name', 'image']

    def validate(self, data):
        user = self.context['request'].user
        if user.team is not None:
            raise serializers.ValidationError('You have to leave your current team first, then you can create a team')

        return data

    def create(self, data):
        current_user = self.context['request'].user
        data['creator'] = current_user

        team = Team.objects.create(**data)
        current_user.team = team
        current_user.save()
        return team
