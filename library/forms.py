# library/forms.py

from django import forms
from .models import CartItem

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
