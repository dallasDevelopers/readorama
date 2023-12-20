import datetime
from django.shortcuts import render
from review.models import Review 
from review.forms import ReviewForm, EditForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from main.models import Books, User 
from django.core import serializers
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required(login_url='/login')
def show_reviews(request):
    review = Review.objects.filter(user=request.user)
    review_counts = review.count()
    is_superuser = request.user.is_superuser
    context = {
        'reviews': review,
        'review_count' : review_counts,
        'is_superuser' : is_superuser,
        'last_login': datetime.datetime.strptime(request.COOKIES['last_login'], '%Y-%m-%d %H:%M:%S.%f'),
    }

    return render(request, 'review_main.html', context)


@login_required(login_url='/login')
def add_reviews(request, id):
    book = Books.objects.get(pk=id)
    users = request.user

    book_title = book.name
    form = ReviewForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        review_title = request.POST.get("review_title")
        review = request.POST.get("review")
        rating = request.POST.get("rating_new")
        new_review = Review(user=users, books=book, review_title=review_title, review=review, rating_new=rating)
        new_review.save()
        return HttpResponseRedirect(reverse('review:review_main'))

    context = {'form': form, 'bookTitle': book_title}
    return render(request, "add_review.html", context)

@login_required(login_url='/login')
def delete_review(request, id):
    # Get data by ID
    review = Review.objects.get(pk=id)
    # Delete data
    review.delete()
    # Return to the main page
    return HttpResponseRedirect(reverse('review:review_main'))

@login_required(login_url='/login')
def edit_review(request, id):
    # Get product by ID
    review = Review.objects.get(pk = id)

    # Set product as instance of form
    form = EditForm(request.POST or None, instance=review)

    if form.is_valid() and request.method == "POST":
        # Save the form and return to home page
        form.save()
        return HttpResponseRedirect(reverse('review:review_main'))

    context = {'form': form, 'ids': id}
    return render(request, "edit_review.html", context)

@login_required(login_url='/login')
def get_review_json(request):
    review_item = Review.objects.filter(user=request.user)
    review_count = review_item.count()
    combined_data = []
    
    for item in review_item:
        book = item.books
        combined_data.append({
            'book_id': book.pk,
            'book_name': book.name,
            'book_author': book.author,
            'book_num_reviews': book.num_review,
            'book_rating': book.rating,
            'book_genre': book.genre,
            'review_title': item.review_title,
            'review': item.review,
            'rating_new' : item.rating_new,
            'review_count' : review_count,
            'review_title': item.review_title,
            'date_added': item.date_added,
            'review_pk' : item.pk,
        })
        
    return JsonResponse(combined_data, safe=False)

def get_review_json_flutter(request, id):
    userdata = User.objects.get(pk=id)
    review_item = Review.objects.filter(user=userdata)
    review_count = review_item.count()
    combined_data = []
    
    for item in review_item:
        book = item.books
        combined_data.append({
            'book_id': book.pk,
            'book_name': book.name,
            'book_author': book.author,
            'book_num_reviews': book.num_review,
            'book_rating': book.rating,
            'book_genre': book.genre,
            'review_title': item.review_title,
            'review': item.review,
            'rating_new' : item.rating_new,
            'review_count' : review_count,
            'review_title': item.review_title,
            'date_added': item.date_added,
            'review_pk' : item.pk,
        })
        
    return JsonResponse(combined_data, safe=False)

@login_required(login_url='/login')
def get_book_id(request, id):
    review_item = Review.objects.filter(pk=id)
    review_count = review_item.count()
    combined_data = []
    
    for item in review_item:
        book = item.books
        combined_data.append({
            'book_id': book.pk,
            'book_name': book.name,
            'book_author': book.author,
            'book_num_reviews': book.num_review,
            'book_rating': book.rating,
            'book_genre': book.genre,
            'review_title': item.review_title,
            'review': item.review,
            'rating_new' : item.rating_new,
            'review_count' : review_count,
            'review_title': item.review_title,
            'review_pk' : item.pk,
        })
        
    return JsonResponse(combined_data, safe=False)


@csrf_exempt
def delete_review_flutter(request, id):
    try:
        # Get data by ID
        review = Review.objects.get(pk=id)
        # Delete data
        review.delete()
        # Return to the main page
        return JsonResponse({"status": "sucess"}, status=200)
    except Review.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Review not found"}, status=404)

    except Exception as e:
            # Handle other exceptions
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
def add_reviews_flutter(request, id):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_review = Review.objects.create(
            review_title= data["reviewTitle"],
            review = data["review"],
            rating_new= float(data["ratingNew"]),
            books = Books.objects.get(pk=id), 
            user = User.objects.get(pk=data['user'])
                   
        )
        new_review.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt

def edit_review_flutter(request, id):
    try:
        review = Review.objects.get(pk=id)
    except Review.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Review not found'}, status=404)

    if request.method == 'POST':
        data = json.loads(request.body)

        print(data)

        review.review_title = data.get("review_title", review.review_title)
        review.review = data.get("review", review.review)
        review.rating_new = data.get("rating_new", review.rating_new)

        book_name = data.get("book_name")
        if book_name is not None:
            try:
                book = Books.objects.filter(name=book_name).first()
                if book is not None:
                    review.books = book
                else:
                    return JsonResponse({'status': 'error', 'message': 'Book not found'}, status=404)
            except Books.MultipleObjectsReturned:
                return JsonResponse({'status': 'error', 'message': 'Multiple books with the same name found'}, status=400)

        review.save()

        return JsonResponse({'status':'success', 'message':'Review successfully edited'})

    return JsonResponse({'status': 'error', 'message':'Invalid request method'}, status=400)

@csrf_exempt
def load_review_id(request, id):

    review_item = Review.objects.filter(pk=id)
    review_count = review_item.count()
    combined_data = []
    
    for item in review_item:
        book = item.books
        combined_data.append({
            'book_id': book.pk,
            'book_name': book.name,
            'book_author': book.author,
            'book_num_reviews': book.num_review,
            'book_rating': book.rating,
            'book_genre': book.genre,
            'review_title': item.review_title,
            'review': item.review,
            'rating_new' : item.rating_new,
            'review_count' : review_count,
            'review_title': item.review_title,
            'date_added': item.date_added,
            'review_pk' : item.pk,
        })
        
    return JsonResponse(combined_data, safe=False)

def load_books_by_id(request, id):
    data = Books.objects.get(pk=id)
    book_name = data.name
    return JsonResponse({'book_name': book_name}, status= 200)