from django.db import models
from django.contrib.auth.models import User
from main.models import Books
# from main import Books

# Create your models here.

class Review(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ForeignKey(Books, on_delete=models.CASCADE)
    review_title = models.CharField(max_length=50)
    review = models.TextField()
    date_added = models.DateField()
    rating_new = models.FloatField()
