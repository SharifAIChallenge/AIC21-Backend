from import_export import resources, fields

from .models import Match


class MatchResource(resources.ModelResource):
    team1 = fields.Field(attribute='team1__name',
                         column_name='team1')
    team2 = fields.Field(attribute='team2__name',
                         column_name='team2')
    winner = fields.Field(attribute='winner__name',
                          column_name='winner')
    game_log = fields.Field()
    server_log = fields.Field()

    class Meta:
        model = Match
        fields = ('team1', 'team2', 'winner', 'infra_token', 'game_log',
                  'server_log')

    def dehydrate_game_log(self, obj: Match):
        return obj.game_log

    def dehydrate_server_log(self, obj: Match):
        return obj.server_log
