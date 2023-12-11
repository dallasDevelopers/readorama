import datetime
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from main.models import Books
from landing_admin.forms import BookForm
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth.decorators import login_required
import json


from functools import wraps
from django.http import HttpResponseForbidden

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access denied. You must be a superuser to access this page.")
    return _wrapped_view


# Create your views here.
@superuser_required
@login_required(login_url='/login')
def show_main(request):
    books = Books.objects.all()
    is_superuser = request.user.is_superuser
    context = {
        'books' : books,
        'appname' : 'ReadORama',
        'is_superuser' : is_superuser,
        'last_login': datetime.datetime.strptime(request.COOKIES['last_login'], '%Y-%m-%d %H:%M:%S.%f'),
    }

    return render(request, ['landingadmin.html', 'base.html'], context)


@superuser_required
@login_required(login_url='/login')
def add_book(request):
    form = BookForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return HttpResponseRedirect(reverse('landing_admin:show_main'))

    context = {'form': form}
    return render(request, "add_book.html", context)

@superuser_required
@login_required(login_url='/login')
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


@superuser_required
@login_required(login_url='/login')
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


@superuser_required
@login_required
def get_product_json(request):
    product_item = Books.objects.all()
    return HttpResponse(serializers.serialize('json', product_item))


@superuser_required
@login_required(login_url='/login')
@csrf_exempt
def delete_ajax(request, id):
    item = Books.objects.get(pk=id)
    item.delete()
    return HttpResponse(b"DELETED", status=201)


@superuser_required
@login_required(login_url='/login')
def get_book_by_id(request, id):
    item = Books.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', item))


@csrf_exempt
def add_product_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_book = Books.objects.create(
            name = data["name"],
            author = data["author"],
            rating = float(data["rating"]),
            num_review = int(data["num_review"]),
            price = int(data["price"]),
            year = int(data["year"]),
            genre = data["genre"]
        )

        new_book.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    

@csrf_exempt
def delete_book_flutter(request, id):
    try:
        # Get product by ID
        book = Books.objects.get(pk=id)

        # Delete the product  
        book.delete()

        return JsonResponse({"status": "success"}, status=200)

    except Books.DoesNotExist:
        # If the product with the given ID does not exist
        return JsonResponse({"status": "error", "message": "Book not found"}, status=404)

    except Exception as e:
        # Handle other exceptions
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
@csrf_exempt
def edit_product_flutter(request, id):
    try:
        book = Books.objects.get(pk=id)
    except Books.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Book not found'}, status=404)

    if request.method == 'PUT':  # Check for PUT method
        data = json.loads(request.body)  # Use request.body to get the data sent via PUT request

        # Update book fields if data is available in the request
        book.name = data.get("name", book.name)
        book.author = data.get("author", book.author)
        book.rating = float(data.get("rating", book.rating))
        book.num_review = int(data.get("num_review", book.num_review))
        book.price = int(data.get("price", book.price))
        book.year = int(data.get("year", book.year))
        book.genre = data.get("genre", book.genre)

        book.save()

        return JsonResponse({"status": "success", "message": "Book updated successfully"})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    

def load_books_by_id(request, id):
    data = Books.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")