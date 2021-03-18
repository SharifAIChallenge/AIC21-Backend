from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.challenge.models import LevelBasedTournament
from apps.team.models import Team


class LevelBasedTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelBasedTournament
        fields = ('tournament', 'size')


class LevelBasedTournamentCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=512)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    is_hidden = serializers.BooleanField()
    is_friendly = serializers.BooleanField(required=False)
    is_scoreboard_freeze = serializers.BooleanField(required=False)
    size = serializers.IntegerField()

    def create(self, validated_data):
        lvl_based_tournament = LevelBasedTournament.create_level_based_tournament(
            name=validated_data.get('name'),
            start_time=validated_data.get('start_time'),
            end_time=validated_data.get('end_time'),
            is_hidden=validated_data.get('is_hidden'),
            is_friendly=validated_data.get('is_friendly'),
            is_scoreboard_freeze=validated_data.get('is_scoreboard_freeze'),
            size=validated_data.get('size'),
        )

        return lvl_based_tournament


class TeamListField(serializers.ListField):
    id = serializers.IntegerField()


class LevelBasedTournamentAddTeamsSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    teams = TeamListField

    def validate(self, attrs):
        get_object_or_404(LevelBasedTournament.objects.all(), pk=attrs['id'])
        teams_list = Team.objects.filter(id__in=attrs['teams'])
        if len(teams_list) != len(attrs['teams']):
            team_list_id = [team.id for team in teams_list]
            invalid_team_list = set(attrs['teams']) - set(team_list_id)

            raise serializers.ValidationError('Invalid Team Ids (' + ', '.join(invalid_team_list) + ')')

        return attrs


    def create(self, validated_data):
        pass

        # TODO : Add a new level and add teams to it and create match 2 by 2