from django.urls import path
from wishlist.views import show_wishlist, add_wishlist

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='wishlist_main'),
    path('add', add_wishlist, name='add_wishlist')
]