from django.urls import path
from landing_admin.views import show_main, add_book_ajax, get_product_json
from landing_admin.views import delete_ajax, get_book_by_id, edit_book, add_product_flutter \
, delete_book_flutter, edit_product_flutter, load_books_by_id, search_books_flutter \
, get_review_json_flutter, load_review_by_id, delete_book_flutter, delete_review_flutter, load_books_by_id_flutter

app_name = 'landing_admin'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add-book-ajax', add_book_ajax, name='add_book_ajax'),
    path('get-product-json', get_product_json, name='get_product_json'),
    path('edit-book/<int:id>', edit_book, name='edit_book'),
    path('delete-ajax/<int:id>', delete_ajax, name="delete_ajax"),
    path('getbook/<int:id>', get_book_by_id, name='get_book_by_id'),
    path('add-book-flutter', add_product_flutter, name="add_book_flutter"),
    path('delete-book-flutter/<int:id>', delete_book_flutter, name="delete_book_flutter"),
    path('edit-product-flutter/<int:id>', edit_product_flutter, name='edit_product_flutter'),
    path('loadbooks-by-id/<int:id>', load_books_by_id, name='loadbooks_by_id'),
    path('search-books-flutter', search_books_flutter, name='search_books_flutter'),
    path('load-all-review', get_review_json_flutter, name='load_all_review'),
    path('delete-review-flutter/<int:id>', delete_review_flutter, name='delete_review_flutter'),
    path('load-review-by-id/<int:id>', load_review_by_id, name='load_review_by_id'),
    path('load-book-flutter/<int:id>', load_books_by_id_flutter, name='load_book_flutter')
]