from django.db import models


class ClanTeam(models.Model):
    clan = models.ForeignKey(to='challenge.Clan', on_delete=models.CASCADE, name='teams')
    team = models.OneToOneField(to='team.Team', on_delete=models.RESTRICT, name='clan')
