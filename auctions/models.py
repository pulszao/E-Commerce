from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=64)
    image = models.URLField(blank=True, null=True)
    creator_id = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

class Bids(models.Model):
    user_id = models.IntegerField()
    listing_title = models.CharField(max_length=64)
    bid = models.IntegerField(blank=False)

class Comments(models.Model):
    user_id = models.IntegerField()
    listing_title = models.CharField(max_length=64)
    comment = models.CharField(max_length=200, blank=False)
    time = models.DateTimeField(auto_now_add=True)
