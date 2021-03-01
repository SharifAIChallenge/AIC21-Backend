from django.db import models


# Create your models here.

class Staff(models.Model):
    group_title = models.CharField(max_length=128)
    team_title = models.CharField(max_length=256, blank=True, null=True)
    first_name_en = models.CharField(max_length=128, null=True, blank=True)
    first_name_fa = models.CharField(max_length=128)
    last_name_en = models.CharField(max_length=128, null=True, blank=True)
    last_name_fa = models.CharField(max_length=128)
    role = models.CharField(max_length=128, blank=True, null=False)
    url = models.CharField(max_length=500, null=True, blank=True)

    def upload_path(self, filename):
        return f'staff/{self.group_title}/{self.team_title}/{filename}'

    image = models.ImageField(upload_to=upload_path)
