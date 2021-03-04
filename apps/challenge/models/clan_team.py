from django.db import models


class ClanTeam(models.Model):
    clan = models.ForeignKey(to='challenge.Clan', on_delete=models.CASCADE, related_name='teams')
    # todo:does it have to be restricted
    team = models.OneToOneField(to='team.Team', on_delete=models.RESTRICT, related_name='clan_team')
