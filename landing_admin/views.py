from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.models import Books
from landing_admin.forms import BookForm
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

# Create your views here.
def show_main(request):
    books = Books.objects.all()
    context = {
        'books' : books,
        'appname' : 'ReadORama'
    }

    return render(request, 'landingadmin.html', context)

def add_book(request):
    form = BookForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return HttpResponseRedirect(reverse('landing_admin:show_main'))

    context = {'form': form}
    return render(request, "add_book.html", context)


@csrf_exempt
def add_book_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        author = request.POST.get("author")
        rating = request.POST.get("rating")
        num_review = request.POST.get("num_review")
        price = request.POST.get("price")
        year = request.POST.get("year")
        genre = request.POST.get("genre")

        new_product = Books(name=name, author=author, rating=rating, 
                            num_review=num_review, price=price, year=year,
                            genre=genre)
        new_product.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()



def edit_book(request, id):
    # Get product by ID
    book = Books.objects.get(pk = id)

    # Set product as instance of form
    form = BookForm(request.POST or None, instance=book)

    if form.is_valid() and request.method == "POST":
        # Save the form and return to home page
        form.save()
        return HttpResponseRedirect(reverse('landing_admin:show_main'))

    context = {'form': form}
    return render(request, "edit_book.html", context)


def get_product_json(request):
    product_item = Books.objects.all()
    return HttpResponse(serializers.serialize('json', product_item))


@csrf_exempt
def delete_ajax(request, id):
    item = Books.objects.get(pk=id)
    item.delete()
    return HttpResponse(b"DELETED", status=201)

def get_book_by_id(request, id):
    item = Books.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', item))