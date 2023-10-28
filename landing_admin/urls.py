from django.urls import path
from landing_admin.views import show_main, add_book_ajax, get_product_json
from landing_admin.views import delete_ajax, get_book_by_id, edit_book

app_name = 'landing_admin'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add-book-ajax', add_book_ajax, name='add_book_ajax'),
    path('get-product-json', get_product_json, name='get_product_json'),
    path('edit-book/<int:id>', edit_book, name='edit_book'),
    path('delete-ajax/<int:id>', delete_ajax, name="delete_ajax"),
    path('getbook/<int:id>', get_book_by_id, name='get_book_by_id'),
]