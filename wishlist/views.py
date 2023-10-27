from django.shortcuts import render
from wishlist.models import Wishlist 
from wishlist.forms import WishlistForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def show_wishlist(request):
    wishlist = Wishlist.objects.all()
    wishlist_count = wishlist.count()
    context = {
        'wishlist' : wishlist,
        'wishlist_count' : wishlist_count
    }

    return render(request, 'wishlist_main.html', context)

def add_wishlist(request):
    form = WishlistForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))  
    
    context = {'form': form}
    return render(request, "add_wishlist.html", context)