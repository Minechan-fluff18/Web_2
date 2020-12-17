from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class ShoppingItem(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    price = models.IntegerField()
    category = models.CharField(max_length=200)
    creator  = models.CharField(max_length=200)
