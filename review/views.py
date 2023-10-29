from django.shortcuts import render
from review.models import Review 
from review.forms import ReviewForm, EditForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from main.models import Books
from django.core import serializers

# Create your views here.

def show_reviews(request):
    review = Review.objects.filter(user=request.user)
    review_counts = review.count()
    context = {
        'reviews': review,
        'review_count' : review_counts
    }

    return render(request, 'review_main.html', context)


def add_reviews(request, id):
    form = ReviewForm(request.POST or None)
    books = Books.objects.filter(pk =id)
    book_title = books.name 
    if form.is_valid() and request.method == "POST":
        review = form.save(commit=False)
        review.user = request.user
        review.books = book_title #Review.objects.get(pk=id)
        review.save()
        return HttpResponseRedirect(reverse('review:review_main'))

    context = {'form': form}
    return render(request, "add_review.html", context)


def delete_review(request, id):
    # Get data by ID
    review = Review.objects.get(pk=id)
    # Delete data
    review.delete()
    # Return to the main page
    return HttpResponseRedirect(reverse('review:review_main'))

def edit_review(request, id):
    # Get product by ID
    review = Review.objects.get(pk = id)

    # Set product as instance of form
    form = ReviewForm(request.POST or None, instance=review)

    if form.is_valid() and request.method == "POST":
        # Save the form and return to home page
        form.save()
        return HttpResponseRedirect(reverse('review:review_main'))

    context = {'form': form, 'ids': id}
    return render(request, "edit_review.html", context)

def get_review_json(request):
    review_item = Review.objects.all()
    return HttpResponse(serializers.serialize('json', review_item))