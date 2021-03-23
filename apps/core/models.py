import os

from django.db import models


# Create your models here.
from rest_framework_tracking.models import APIRequestLog


class File(models.Model):
    def upload_path(self, filename):
        return os.path.join('core', 'storage', filename)

    file = models.FileField(upload_to=upload_path)

    def __str__(self):
        return f'id: {self.id}, filename: {self.file.name}'


class APIRequestLogProxy(APIRequestLog):
    class Meta:
        proxy = True
