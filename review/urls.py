from django.urls import path
from review.views import show_reviews, add_reviews

app_name = 'review'

urlpatterns = [
    path('', show_reviews, name='review_main'),
    path('add', add_reviews, name='add_reviews')
]