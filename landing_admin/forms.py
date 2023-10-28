from django.forms import ModelForm
from main.models import Books

class BookForm(ModelForm):
    class Meta:
        model = Books
        fields = ["name", "author", "rating", "num_review", "price", 'year', 'genre']