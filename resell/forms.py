from django import forms
from .models import Product
from taggit.forms import TagWidget
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'high_price', 'quantity', 'currency', 'unit', 'categories']

        widgets = {
            'categories': TagWidget(),
        }