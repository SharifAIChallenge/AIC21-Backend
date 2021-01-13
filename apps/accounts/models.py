from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birth_date = models.CharField(
        max_length=128
    )
    province = models.CharField(
        max_length=128
    )
