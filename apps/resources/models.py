from django.db import models

# Create your models here.

class Resource(models.Model):
    title = models.CharField(max_length=50)
    description= models.TextField(max_length=1000)

    def __str__(self):
        return '%s' % (self.title)


class DownloadLink(models.Model):
    url = models.URLField(max_length=500)
    title = models.CharField(max_length=50)
    resource = models.ForeignKey(to=Resource,on_delete=models.CASCADE,related_name='links')

