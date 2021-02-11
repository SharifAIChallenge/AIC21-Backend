from django.db import models


# Create your models here.
class Gamedoc(models.Model):
    link = models.URLField(max_length=500)
    title = models.CharField(max_length=500)

    def __str__(self):
        return '%s' % (self.title)
