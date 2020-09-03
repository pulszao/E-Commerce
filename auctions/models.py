from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    image = models.URLField(blank=True)
    creator = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)

class Bids(models.Model):
    username = models.CharField(max_length=32)
    starting_bid = models.IntegerField()
    heighest_bid = models.IntegerField()

class Comments(models.Model):
    username = models.CharField(max_length=32)
    comment = models.CharField(max_length=200)