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

    def clean_quantity(self):
        cd = self.cleaned_data
        quantity = cd['quantity']
        product = self.cleaned_data.get('product')

        if quantity and (quantity > product.remaining_stock()):
            raise forms.ValidationError('Not enough quantity available for this product.')
        if quantity <= 0:
            raise forms.ValidationError('Must be greater than 0')
        return quantity
