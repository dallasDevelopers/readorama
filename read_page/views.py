from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.core import serializers
from wishlist.models import Wishlist 
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def show_xml(request):
    data = Wishlist.objects.filter(user=request.user, flag = True)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required(login_url='/login')
def show_json(request):
    data = Wishlist.objects.filter(user=request.user, flag = True)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login')
def show_xml_by_id(request, id):
    data = Wishlist.objects.filter(user=request.user, flag = True, pk = id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required(login_url='/login')
def show_json_by_id(request, id):
    data = Wishlist.objects.filter(user=request.user, flag = True, pk = id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login')
@csrf_exempt
def delete_product(request, id):
    data = get_object_or_404(Wishlist, user=request.user, flag=True, pk=id)
    data.delete()
    return HttpResponse(b"DELETED", status=201)

def get_product_json(request):
    product_item = Wishlist.objects.filter(user=request.user, flag = True)
    return HttpResponse(serializers.serialize('json', product_item))