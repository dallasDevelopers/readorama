from django.shortcuts import render
from review.models import Review 
from review.forms import ReviewForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def show_reviews(request):
    review = Review.objects.all()
    review_counts = review.count()
    context = {
        'reviews': review,
        'review_count' : review_counts
    }

    return render(request, 'review_main.html', context)


def add_reviews(request):
    form = ReviewForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "add_review.html", context)