from behave import When
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from sqlparse.sql import Case

from apps.challenge.models import LevelBasedTournament, Match, Map, LevelMatch, Level
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

        if len(attrs['teams']) % 2 == 1:
            raise Exception('Teams list size must be even not odd!')

        teams_list = Team.objects.filter(id__in=attrs['teams'])
        if len(teams_list) != len(attrs['teams']):
            team_list_id = [team.id for team in teams_list]
            invalid_team_list = set(attrs['teams']) - set(team_list_id)

            raise serializers.ValidationError('Invalid Team Ids (' + ', '.join(invalid_team_list) + ')')

        return attrs


    def create(self, validated_data):
        level_based_tournament = get_object_or_404(LevelBasedTournament.objects.all(), pk=validated_data.id)

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(validated_data.teams)])
        teams = Team.objects.filter(id__in=validated_data.teams).order_by(preserved)
        # TODO : Check the order is the same ...

        random_map = Map.get_random_map()
        matches = Match.create_match_from_list(teams, level_based_tournament.tournament, random_map)

        last_level = LevelBasedTournament.last_level
        new_level = Level.objects.create(
            last_level.number + 1,
            level_based_tournament
        )

        level_matches = LevelMatch.create_level_matches(matches, new_level)

