from django.shortcuts import render

# Create your views here.

def show_main(request):
    
    context = {
        'appname': 'ReadORama',
    }

    return render(request, 'main.html', context)