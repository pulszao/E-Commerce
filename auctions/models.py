from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    price = models.IntegerField()
    description = models.CharField(max_length=2500)
    image = models.URLField(blank=True)
    starting_bid = models.IntegerField()
    highest_bid = models.IntegerField()
    creator = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)