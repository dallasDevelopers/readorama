from django.urls import path
from landing_admin.views import show_main, add_book, add_book_ajax

app_name = 'landing_user'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add', add_book, name='add_book'),
    path('add-ajax', add_book_ajax, name='add_book_ajax'),
]