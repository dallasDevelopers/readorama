from django.shortcuts import render
from main.models import Books
from main.forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpResponse
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login')
def show_main(request):

    dataAll = Books.objects.all().order_by('-rating')
    
    context = {
        'appname': 'ReadORama',
        'datas': dataAll,
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