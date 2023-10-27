from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.core import serializers
from wishlist.models import Wishlist 

# Create your views here.

def show_read_page(request):
    readBooks = Wishlist.objects.filter(flag = True)
    readBooks_count = readBooks.count()
    is_superuser = request.user.is_superuser
    context = {
        'appname': 'read_page',
        'readBooks' : readBooks,
        'readBooks_count' : readBooks_count,
        'is_superuser' : is_superuser,
    }

    return render(request, 'read_page.html', context)   

def delete_product(request, id):
    readBooks = Wishlist.objects.filter(flag = True)
    # Get data by ID
    product = readBooks.objects.get(pk=id)
    # Delete data
    product.delete()
    # Return to the main page
    return HttpResponseRedirect(reverse('read_page:show_read_page'))

def show_xml(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")