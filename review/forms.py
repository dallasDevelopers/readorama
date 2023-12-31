from django.forms import ModelForm, widgets
from django import forms
from review.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['review_title', 'review', 'rating_new']

        # widgets = {
        #     'review_title' : forms.TextInput(attrs={'class' : 'form-control', 'name': 'review_title'}),
        #     'review' : forms.TextInput(attrs={'class' : 'form-control', 'name': 'review'}), 
        #     'books' : forms.TextInput(attrs={'class' : 'form-control', 'name' : 'books', 'value': 'book_title'}), 
        #     'rating_new' : forms.NumberInput(attrs={'class' : 'form-control', 'name': 'rating_new'})
        # }

class EditForm(ModelForm):
    class Meta:
        model = Review
        fields = ['review_title', 'review', 'rating_new']
        widgets = {
            'review_title' : forms.TextInput(attrs={'class' : 'form-control', 'name': 'review_title'}),
            'review' : forms.Textarea(attrs={'class' : 'form-control', 'name': 'review'}), 
            'rating_new' : forms.NumberInput(attrs={'class' : 'form-control', 'name': 'rating_new', 'min':'1', 'max': '5'})
        }