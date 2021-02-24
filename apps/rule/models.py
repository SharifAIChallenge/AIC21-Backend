from django.db import models

class Rule(models.Model):
    title_en = models.CharField(max_length=50, blank=True)
    title_fa = models.CharField(max_length=50)
    text_en = models.TextField(max_length=10000, blank=True)
    text_fa = models.TextField(max_length=10000)
    order = models.IntegerField(default=0)

    def __str__(self):
        return '%s (%s)' % (self.title_en, self.title_fa)