from django.shortcuts import render
from main.models import Books

# Create your views here.

def show_main(request):
    
    context = {
        'appname': 'ReadORama',
    }

    return render(request, 'main.html', context)