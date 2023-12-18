from django.shortcuts import render
from main.models import Books
from main.forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from landing_admin.views import show_main
from wishlist.models import Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url='/login')
def show_main(request):

    dataAll = Books.objects.all().order_by('-rating')
    is_superuser = request.user.is_superuser
    
    context = {
        'appname': 'ReadORama',
        'datas': dataAll,
        'is_superuser' : is_superuser,
        'last_login': datetime.datetime.strptime(request.COOKIES['last_login'], '%Y-%m-%d %H:%M:%S.%f'),
    }

    return render(request, 'main.html', context)

def load_books(request):
    data = Books.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def register(request):
    form = UserCreationForm()
    msg = None
    # success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    context = {"form": form, "msg": msg}
    return render(request, "register.html", context)

@csrf_exempt
def login_user(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))

            if user.is_superuser:
                response = HttpResponseRedirect(reverse("landing_admin:show_main"))

            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            msg = messages.info(request, 'Sorry, incorrect username or password. Please try again.')

    context = {"form": form, "msg": msg}
    return render(request, 'login.html', context)

@csrf_exempt
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def search_books(request):
    search_term = request.GET.get('search_term', '')
    filtered_books = Books.objects.filter(name__icontains=search_term)
    book_data = [{'name': book.name, 'author': book.author, 'num_reviews': book.num_review, 'rating': book.rating, 'genre': book.genre, 'bookid':book.id} for book in filtered_books]
    return JsonResponse({'datas': book_data})

def search_books_blank(request):
    search_term = request.GET.get('search_term', '')
    filtered_books = Books.objects.filter(name__icontains=search_term).order_by('-rating')
    book_data = [{'name': book.name, 'author': book.author, 'num_reviews': book.num_review, 'rating': book.rating, 'genre': book.genre, 'bookid':book.id} for book in filtered_books]
    return JsonResponse({'datas': book_data})

def addToWishlist(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id', '')
        user = request.user

        try:
            
            book = Books.objects.get(pk=book_id)
            wishlist, created = Wishlist.objects.get_or_create(user=user, books=book, flag=False)

            if created:
                response_data = {'message': 'Book added to wishlist successfully'}
            else:
                response_data = {'message': 'Book is already in your wishlist'}

        except Books.DoesNotExist:
            response_data = {'message': 'Book not found'}

        return JsonResponse(response_data)

    return JsonResponse({'message': 'Invalid request method'})

def bookReaded(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id', '')
        user = request.user
        try:
            
            book = Books.objects.get(pk=book_id)
            wishlist, created = Wishlist.objects.get_or_create(user=user, books=book, flag=True)

            if created:
                response_data = {'message': 'Book marked as read successfully'}
            else:
                response_data = {'message': 'Book already marked as read'}

        except Books.DoesNotExist:
            response_data = {'message': 'Book not found'}

        return JsonResponse(response_data)

    return JsonResponse({'message': 'Invalid request method'})


def filter_books_by_category(request):
    category = request.GET.get('category', 'all')

    if category == 'all':
        books = Books.objects.all().order_by('-rating')
    elif category == 'Fiction':
        books = Books.objects.exclude(genre__icontains='Non').order_by('-rating')
    elif category == 'Non Fiction':
        books = Books.objects.filter(genre__icontains='Non').order_by('-rating')
    else:
        return JsonResponse({'error': 'Invalid category'})

    book_data = []

    for book in books:
        book_data.append({
            'bookid': book.pk,
            'name': book.name,
            'author': book.author,
            'num_reviews': book.num_review,
            'rating': book.rating,
            'genre': book.genre,
        })

    return JsonResponse({'datas': book_data})

@csrf_exempt
def search_booksflutter(request):
    search_term = request.GET.get('search_term', '')
    filtered_books = Books.objects.filter(name__icontains=search_term)
    
    book_data = []
    for book in filtered_books:
        book_entry = {
            "model": "main.books",
            "pk": book.pk,
            "fields": {
                "name": book.name,
                "author": book.author,
                "rating": book.rating,
                "num_review": book.num_review,
                "price": book.price,
                "year": book.year,
                "genre": book.genre
            }
        }
        book_data.append(book_entry)

    return JsonResponse(book_data, safe=False)

@csrf_exempt
def addToWishlistFlutter(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_pk', '')
        user = request.POST.get('user_id', '')

        try:
            
            book = Books.objects.get(pk=book_id)
            userdata = User.objects.get(pk=user)
            wishlist, created = Wishlist.objects.get_or_create(user=userdata, books=book, flag=False)

            if created:
                response_data = {'message': 'Book added to wishlist successfully'}
            else:
                response_data = {'message': 'Book is already in your wishlist'}

        except Books.DoesNotExist:
            response_data = {'message': 'Book not found'}

        return JsonResponse(response_data)

    return JsonResponse({'message': 'Invalid request method'})
# test
@csrf_exempt
def markAsReadFlutter(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_pk', '')
        user = request.POST.get('user_id', '')

        try:
            
            book = Books.objects.get(pk=book_id)
            userdata = User.objects.get(pk=user)
            wishlist, created = Wishlist.objects.get_or_create(user=userdata, books=book, flag=True)

            if created:
                response_data = {'message': 'Book marked as read successfully'}
            else:
                response_data = {'message': 'Book already marked as read'}

        except Books.DoesNotExist:
            response_data = {'message': 'Book not found'}

        return JsonResponse(response_data)

    return JsonResponse({'message': 'Invalid request method'})

def show_wishlist(request):
    wishlist = Wishlist.objects.all()
    return HttpResponse(serializers.serialize("json", wishlist), content_type="application/json")