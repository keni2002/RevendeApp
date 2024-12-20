from django import forms

from sale.models import SaleProduct
from .models import Product
from taggit.forms import TagWidget
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'high_price', 'quantity', 'currency', 'unit', 'categories']

        widgets = {
            'categories': TagWidget(),
        }

class ProductSellForm(forms.ModelForm):
    class Meta:
        model = SaleProduct
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return quantity