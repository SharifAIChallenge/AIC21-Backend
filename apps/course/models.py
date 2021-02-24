from django.db import models

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)