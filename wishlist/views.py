from django.shortcuts import render
from wishlist.models import Wishlist 
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def show_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    wishlist_count = wishlist.count()
    context = {
        'wishlist' : wishlist,
        'wishlist_count' : wishlist_count
    }

    return render(request, 'wishlist_main.html', context)

def delete_wishlist(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id)

    if request.method == "POST":
        wishlist.delete()
        messages.success(request, 'Wishlist item deleted successfully.')
        return redirect('wishlist:show_wishlist')

    context = {'wishlist': wishlist}
    return render(request, "delete_wishlist.html", context)

def show_xml(request):
    data = Wishlist.objects.all()
    return HttpResponse(
        serializers.serialize("xml", data), content_type="application/xml"
    )


def show_json(request):
    data = Wishlist.objects.all()
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )


def show_xml_by_id(request, id):
    data = Wishlist.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("xml", data), content_type="application/xml"
    )


def show_json_by_id(request, id):
    data = Wishlist.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )

def get_product_json(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", wishlist))

@csrf_exempt
def delete_product_ajax(request, id):
    product = Wishlist.objects.get(pk=id)
    product.delete()
    return HttpResponse(b"DELETED", status=201)