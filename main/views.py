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

# Create your views here.

@login_required(login_url='/login')
def show_main(request):

    dataAll = Books.objects.all().order_by('-rating')
    
    context = {
        'appname': 'ReadORama',
        'datas': dataAll,
        'last_login': datetime.datetime.strptime(request.COOKIES['last_login'], '%Y-%m-%d %H:%M:%S.%f'),
    }

    return render(request, 'main.html', context)

def load_books(request):
    data = Books.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def search_books(request):
    search_term = request.GET.get('search_term', '')
    filtered_books = Books.objects.filter(name__icontains=search_term)
    book_data = [{'name': book.name, 'author': book.author, 'num_reviews': book.num_review, 'rating': book.rating, 'genre': book.genre} for book in filtered_books]
    return JsonResponse({'datas': book_data})

def search_books_blank(request):
    search_term = request.GET.get('search_term', '')
    filtered_books = Books.objects.filter(name__icontains=search_term).order_by('-rating')
    book_data = [{'name': book.name, 'author': book.author, 'num_reviews': book.num_review, 'rating': book.rating, 'genre': book.genre, 'bookid':book.id} for book in filtered_books]
    return JsonResponse({'datas': book_data})

from django.http import JsonResponse

def addToWishlist(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id', '')  # Dapatkan ID buku dari permintaan POST
        user = request.user  # Dapatkan pengguna yang saat ini masuk

        try:
            # Cari buku dengan ID yang diberikan
            book = Books.objects.get(pk=book_id)

            # Cek apakah buku ini sudah ada dalam wishlist pengguna
            wishlist, created = Wishlist.objects.get_or_create(user=user, books=book, flag=False)

            if created:
                # Buku berhasil ditambahkan ke wishlist
                response_data = {'message': 'Book added to wishlist successfully'}
            else:
                # Buku sudah ada dalam wishlist pengguna
                response_data = {'message': 'Book is already in your wishlist'}

        except Books.DoesNotExist:
            # Buku dengan ID yang diberikan tidak ditemukan
            response_data = {'message': 'Book not found'}

        return JsonResponse(response_data)

    # Handle other HTTP methods (e.g., GET) if needed
    return JsonResponse({'message': 'Invalid request method'})

