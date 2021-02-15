from django.db import models
import os

# Create your models here.


# TODO : Create a TimeStampable for created_at and updated_at fields
class Team(models.Model): 
    name = models.CharField(max_length=128, unique=True)
    image = models.ImageField(upload_to="teams/images/", null=True, blank=True) # TODO : Should read path from setting parameters
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    creator_email = models.CharField(max_length=254)

    def __str__(self):
        return '%s' % self.name 