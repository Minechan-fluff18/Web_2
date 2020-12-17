from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    login    = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    email    = models.CharField(max_length=200, unique=True)
    likes    = ArrayField(
        models.IntegerField(),
        blank=True,
        null=True
        )
