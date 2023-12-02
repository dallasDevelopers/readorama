from django.urls import path
from authentication.views import login, logout, registerflutter

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', registerflutter, name='register'),
]