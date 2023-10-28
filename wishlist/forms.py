from django.forms import ModelForm
from wishlist.models import Wishlist

class WishlistForm(ModelForm):
    class Meta:
        model = Wishlist
        fields = ["books"]