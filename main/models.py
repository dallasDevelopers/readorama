from django.db import models
from django.contrib.auth.models import User

class Books(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=50, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    review = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    genre = models.TextField(null=True, blank=True)