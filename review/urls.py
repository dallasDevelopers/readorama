from django.urls import path
from review.views import show_reviews, add_reviews, delete_review, edit_review, get_review_json, get_book_id, get_review_json_flutter, delete_review_flutter, add_reviews_flutter, edit_review_flutter, load_review_id, load_books_by_id

app_name = 'review'

urlpatterns = [
    path('', show_reviews, name='review_main'),
    path('add/<int:id>', add_reviews, name='add_reviews'),
    path('delete/<int:id>', delete_review, name='delete_review'),
    path('edit-review/<int:id>', edit_review, name='edit_review'),
    path('get-review/', get_review_json, name='get_review_json'),
    path('get-book/<int:id>', get_book_id, name='get_book_id' ),
    path('get-review-flutter/<int:id>/', get_review_json_flutter, name='get_review_json_flutter' ),
    path('delete-review-flutter/<int:id>', delete_review_flutter, name='delete_review_flutter' ),
    path('add-review-flutter/<int:id>', add_reviews_flutter, name='add_review_flutter' ),
    path('edit-review-flutter/<int:id>', edit_review_flutter, name='edit_review_flutter' ), 
    path('load-review-id/<int:id>', load_review_id, name='load_review_id'), 
    path('load-books-id/<int:id>', load_books_by_id, name='load_books_id')
]