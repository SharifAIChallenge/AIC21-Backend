from django.db import models


# Create your models here.
class Gamedoc(models.Model):
    link = models.URLField(max_length=500)
    title = models.CharField(max_length=500)
    repo_name = models.CharField(max_length=512, blank=True, null=True)
    user_name = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'
