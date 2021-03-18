from rest_framework import serializers

from apps.challenge.models import LevelBasedTournament


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