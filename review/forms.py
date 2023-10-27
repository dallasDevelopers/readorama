from django.forms import ModelForm
from review.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["books", "review_title", "review", "date_added", "rating_new"]