from django.urls import path
from review.views import show_reviews, add_reviews, delete_review, edit_review

app_name = 'review'

urlpatterns = [
    path('', show_reviews, name='review_main'),
    path('add/', add_reviews, name='add_reviews'),
    path('delete/<int:id>', delete_review, name='delete_review'),
    path('edit-product/<int:id>', edit_review, name='edit_review'),
]