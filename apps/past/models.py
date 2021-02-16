from django.db import models

# Create your models here.

class Past(models.Model):
    image = models.ImageField()
    title_en = models.CharField(max_length=50, blank=True)
    title_fa = models.CharField(max_length=50)
    description_en = models.TextField(max_length=1000, blank=True)
    description_fa = models.TextField(max_length=1000)
    firstTeam = models.TextField(max_length=50)
    secondTeam = models.TextField(max_length=50)
    thirdTeam = models.TextField(max_length=50)

    def __str__(self):
        return '%s (%s) [ %s - %s - %s ]' % (self.title_en, self.title_fa,self.firstTeam, self.secondTeam, self.thirdTeam)
