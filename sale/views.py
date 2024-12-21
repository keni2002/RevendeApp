from django  import forms
from django.conf import settings
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Sale

@login_required
def sale_list(request):
    query = request.GET.get('q', '')
    sale_list = Sale.objects.filter(user=request.user)

    if query:
        sale_list = sale_list.filter(
            Q(customer__name__icontains=query) |
            Q(products__name__icontains=query)
        ).distinct()

    items_per_page = request.GET.get('items_per_page', 5)

    order_by = request.GET.get('order_by', 'created')
    ordering = request.GET.get('ordering', 'desc')
    valid_order_fields = ['customer__name', 'created', 'updated', 'total_price', 'total_profit']

    if order_by not in valid_order_fields:
        order_by = 'created'

    if ordering == 'desc':
        order_by = f'-{order_by}'

    sale_list = sale_list.order_by(order_by)

    paginator = Paginator(sale_list, items_per_page)

    page_number = request.GET.get('page', 1)
    try:
        sales = paginator.page(page_number)
    except PageNotAnInteger:
        sales = paginator.page(1)
    except EmptyPage:
        sales = paginator.page(paginator.num_pages)


    class Currency:
        def __init__(self, typos, values):
            self.values = values
            self.typos = typos

    dollar_change = [Currency("USD_TO_CUP",settings.USD_TO_CUP),
                     Currency("EUR_TO_CUP",settings.EUR_TO_CUP),
                     Currency("MLC_TO_CUP",settings.MLC_TO_CUP),]

    return render(request, 'sales/sale_list.html', {
        'sales': sales,
        'items_per_page': items_per_page,
        'order_by': order_by.lstrip('-'),
        'ordering': 'desc' if order_by.startswith('-') else 'asc',
        'query': query,
        'section': 'sales',
        'dollar_change': dollar_change,
    })


# views.py en la aplicación de Sales
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Sale, SaleProduct
from .forms import SaleForm, SaleProductForm
from customer.models import Customer
from product.models import Product

@transaction.atomic
@login_required
def sale_create(request):
    SaleProductFormSet = inlineformset_factory(Sale, SaleProduct, form=SaleProductForm, extra=1, can_delete=True)
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        formset = SaleProductFormSet(request.POST)

        if sale_form.is_valid() and formset.is_valid():
            products_selected  = []
            for index,form in enumerate(formset):
                if not form.cleaned_data or not form.cleaned_data['product']:
                    messages.error(request,f"The form {index+1} is empty.")
                    return render(request, 'sales/sale_form.html', {
                        'sale_form': sale_form,
                        'formset': formset,
                        'customers': Customer.objects.all(),
                        'products': Product.objects.all()
                    })
                if form.cleaned_data['product'] in products_selected:
                    messages.error(request,f"The product {form.cleaned_data['product']} already selected.")
                    return render(request, 'sales/sale_form.html', {
                        'sale_form': sale_form,
                        'formset': formset,
                        'customers': Customer.objects.all(),
                        'products': Product.objects.all()
                    })
                products_selected.append(form.cleaned_data['product'])

            sale = sale_form.save(commit=False)
            sale.total_profit = 0
            sale.total_price = 0
            sale.user = request.user
            sale.save()  # Guardar la venta primero

            total_price = 0
            total_profit = 0
            products = []
            for form in formset:
                sale_product = form.save(commit=False)
                sale_product.sale = sale
                sale_product.save()
                total_price += sale_product.total_price
                total_profit += sale_product.total_profit
                    # Update sold_quantity
                product = sale_product.product
                product.sold_quantity += sale_product.quantity
                product.save()
            # Update total price and profit for the sale
            sale.total_price = total_price
            sale.total_profit = total_profit
            sale.save()

            messages.success(request, "Sale was created successfully!")
            return redirect('sales:sale_list')
        else:
            # If the form or formset is not valid, render the form again with errors
            return render(request, 'sales/sale_form.html',
                          { 'sale_form': sale_form, 'formset': formset, })
    else:
        sale_form = SaleForm()
        formset = SaleProductFormSet()
        return render(request, 'sales/sale_form.html', {
            'sale_form': sale_form,
            'formset': formset,
        })


@login_required
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk, user=request.user)
    if request.method == 'POST':
        sale.delete()
        messages.success(request, "The Sale has been deleted successfully!")
        return redirect('sales:sale_list')
    return render(request, 'sales/sale_confirm_delete.html', {'sale': sale})