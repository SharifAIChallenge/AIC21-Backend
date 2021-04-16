from django.db import models


class League(models.Model):
    tournament_name = models.CharField(max_length=512)

    start_time = models.DateTimeField()
    match_map = models.ForeignKey('challenge.Map', related_name='leagues',
                                  on_delete=models.DO_NOTHING)
    total_matches = models.PositiveIntegerField(default=0)
    run = models.BooleanField(default=False)

    def pre_save(self):
        from apps.challenge.models import Tournament
        from apps.team.models import Team

        if not self.id:
            queryset = Team.humans.all()

            teams = [
                team for team in
                filter(lambda team: team.has_final_submission(), queryset)
            ]

            tournament = Tournament.create_tournament(
                name=self.tournament_name,
                start_time=self.start_time,
                end_time=None,
                is_hidden=False,
                team_list=teams
            )

        if self.run:
            tournament = Tournament.objects.get(name=self.tournament_name)
            self.total_matches = \
                tournament.make_league_for_tournament(match_map=self.match_map)

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)
