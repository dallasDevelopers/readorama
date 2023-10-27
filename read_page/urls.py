from django.urls import path
from read_page.views import show_read_page, show_xml, show_json, show_xml_by_id, show_json_by_id, delete_product

app_name = 'read_page'

urlpatterns = [
    path('', show_read_page, name='show_read_page'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
]