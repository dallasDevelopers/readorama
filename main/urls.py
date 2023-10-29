from django.urls import path, include
from main.views import show_main, register, login_user, logout_user, load_books, search_books, search_books_blank, addToWishlist

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('loadbooks/', load_books, name='load_books'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('search-books/', search_books, name='search_books'),
    path('search-books-blank/', search_books_blank, name='search_books'),
    path('add-to-wishlist/', addToWishlist, name='add_to_wishlist'),
]