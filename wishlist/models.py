from django.db import models
from django.contrib.auth.models import User
from main.models import Books

class Wishlist(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ForeignKey(Books, on_delete=models.CASCADE)
    flag = models.BooleanField(default=False)