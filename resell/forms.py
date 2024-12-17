from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'retailer', 'price', 'high_price', 'quantity', 'currency', 'unit', 'categories']
        widgets = {'categories': forms.TextInput(attrs={'placeholder': 'Categories separated by comma'})}