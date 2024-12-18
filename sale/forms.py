from django import forms
from .models import Sale, SaleProduct

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer']

class SaleProductForm(forms.ModelForm):
    class Meta:
        model = SaleProduct
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
