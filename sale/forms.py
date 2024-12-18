# forms.py en la aplicación de Sales
from django import forms
from .models import Sale, SaleProduct
from customer.models import Customer
from product.models import Product

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer']

class SaleProductForm(forms.ModelForm):
    class Meta:
        model = SaleProduct
        fields = ['product', 'quantity']

    def clean_quantity(self):
        cd = self.cleaned_data
        quantity = cd['quantity']
        product = cd['product']
        if quantity and (quantity > product.remaining_stock):
            raise forms.ValidationError('Not enough quantity available for this product.')
        if quantity <= 0:
            raise forms.ValidationError('Must be greater than 0')
        return quantity

SaleProductFormSet = forms.inlineformset_factory(Sale, SaleProduct, form=SaleProductForm, extra=1, can_delete=True)
