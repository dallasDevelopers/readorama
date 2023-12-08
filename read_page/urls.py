from django.urls import path
from read_page.views import show_read_page, show_xml, show_json, show_xml_by_id, show_json_by_id, delete_product, get_product_json, delete_product_flutter

app_name = 'read_page'

urlpatterns = [
    path('', show_read_page, name='show_read_page'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('delete/<int:id>', delete_product, name='delete_product'),
    path('get-product/', get_product_json, name='get_product_json'),
    path('delete-flutter/<int:id>', delete_product_flutter, name='delete_product_flutter'),
]