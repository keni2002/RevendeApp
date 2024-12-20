from django import forms
from .models import Sale, SaleProduct
from product.models import Product

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer']

#-----------------------------------------------------------------

class SaleProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = SaleProduct
        fields = ['product', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_product(self):
        product = self.cleaned_data.get('product')
        if product is None:
            raise forms.ValidationError("No product selected")
        return product

    def clean_quantity(self):
        cd = self.cleaned_data
        quantity = cd.get('quantity')
        product = cd.get('product')
        if product:
            if quantity and (quantity > product.remaining_stock()):
                raise forms.ValidationError('Not enough quantity available for this product.')
        if quantity <= 0:
            raise forms.ValidationError('Must be greater than 0')
        return quantity


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].label_from_instance = lambda obj: f"{obj.name} [{obj.remaining_stock()}]"
