from django.urls import path
from review.views import show_reviews, add_reviews, delete_review, edit_review, get_review_json, get_book_id

app_name = 'review'

urlpatterns = [
    path('', show_reviews, name='review_main'),
    path('add/<int:id>', add_reviews, name='add_reviews'),
    path('delete/<int:id>', delete_review, name='delete_review'),
    path('edit-review/<int:id>', edit_review, name='edit_review'),
    path('get-review/', get_review_json, name='get_review_json'),
    path('get-book/<int:id>', get_book_id, name='get_book_id' )
]