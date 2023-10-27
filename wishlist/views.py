from django.shortcuts import render
from wishlist.models import Wishlist 
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.
@login_required(login_url='/login')
def show_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user, flag=False)
    wishlist_count = wishlist.count()
    is_superuser = request.user.is_superuser
    context = {
        'wishlist' : wishlist,
        'wishlist_count' : wishlist_count,
        'is_superuser' : is_superuser,
    }

    return render(request, 'wishlist_main.html', context)

@login_required(login_url='/login')
def delete_wishlist(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id)

    if request.method == "POST":
        wishlist.delete()
        messages.success(request, 'Wishlist item deleted successfully.')
        return redirect('wishlist:show_wishlist')

    context = {'wishlist': wishlist}
    return render(request, "delete_wishlist.html", context)

@login_required(login_url='/login')
def show_xml(request):
    data = Wishlist.objects.all()
    return HttpResponse(
        serializers.serialize("xml", data), content_type="application/xml"
    )

@login_required(login_url='/login')
def show_json(request):
    data = Wishlist.objects.all()
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )

@login_required(login_url='/login')
def show_xml_by_id(request, id):
    data = Wishlist.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("xml", data), content_type="application/xml"
    )

@login_required(login_url='/login')
def show_json_by_id(request, id):
    data = Wishlist.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )

@login_required(login_url='/login')
def get_product_json(request):
    wishlist = Wishlist.objects.filter(user=request.user, flag=False)
    return HttpResponse(serializers.serialize("json", wishlist))

@login_required(login_url='/login')
@csrf_exempt
def delete_product_ajax(request, id):
    product = Wishlist.objects.get(pk=id)
    product.delete()
    return HttpResponse(b"DELETED", status=201)

@require_POST
def mark_as_read(request, book_id):
    wishlist_item = Wishlist.objects.get(id=book_id)
    wishlist_item.flag = True
    wishlist_item.save()
    return JsonResponse({'message': 'Book marked as read'})