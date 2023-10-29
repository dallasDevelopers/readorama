from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.core import serializers
from wishlist.models import Wishlist 

# Create your views here.

def show_read_page(request):
    readBooks = Wishlist.objects.filter(user=request.user, flag = True)
    readBooks_count = readBooks.count()
    is_superuser = request.user.is_superuser
    context = {
        'appname': 'read_page',
        'readBooks' : readBooks,
        'readBooks_count' : readBooks_count,
        'is_superuser' : is_superuser,
    }

    return render(request, 'read_page.html', context)   

@csrf_exempt
def delete_product(request, id):
    readBooks = Wishlist.objects.filter(user=request.user, flag = True)
    data = readBooks.objects.get(pk=id)
    data.delete()
    return HttpResponse(b"DELETED", status=201)

def show_xml(request):
    data = Wishlist.objects.filter(user=request.user, flag = True)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Wishlist.objects.filter(user=request.user, flag = True)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Wishlist.objects.filter(user=request.user, flag = True, pk = id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Wishlist.objects.filter(user=request.user, flag = True, pk = id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_product_json(request):
    product_item = Wishlist.objects.filter(user=request.user, flag = True)
    return HttpResponse(serializers.serialize('json', product_item))