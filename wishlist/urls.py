from django.urls import path
from wishlist.views import show_wishlist, delete_wishlist, show_xml, show_json, show_xml_by_id, show_json_by_id, get_product_json, delete_product_ajax, mark_as_read, wishlistmodels

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='wishlist_main'),
    path('delete/<int:wishlist_id>/', delete_wishlist, name='delete_wishlist'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path("get-product/", get_product_json, name="get_product_json"),
    path(
        "delete-product-ajax/<int:id>", delete_product_ajax, name="delete_product_ajax"
    ),
    path('mark-as-read/<int:book_id>/', mark_as_read, name='mark_as_read'),
    path('wishlistmodels/<int:id>/', wishlistmodels, name='wishlist_models'),
]