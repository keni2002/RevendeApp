from django  import forms
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
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

    return render(request, 'sales/sale_list.html', {
        'sales': sales,
        'items_per_page': items_per_page,
        'order_by': order_by.lstrip('-'),
        'ordering': 'desc' if order_by.startswith('-') else 'asc',
        'query': query,
        'section': 'sales'
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
            for index,form in enumerate(formset):
                if not form.cleaned_data or not form.cleaned_data['product']:
                    messages.error(request,f"The form {index+1} is empty.")
                    return render(request, 'sales/sale_form.html', {
                        'sale_form': sale_form,
                        'formset': formset,
                        'customers': Customer.objects.all(),
                        'products': Product.objects.all()
                    })

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
    #
    #
    #         for sale_product_form in saleproduct_formset:
    #             if sale_product_form.cleaned_data:
    #                 product = sale_product_form.cleaned_data['product']
    #                 quantity = sale_product_form.cleaned_data['quantity']
    #
    #                 if product in products:
    #                     messages.error(request,
    #                                    "You have selected the same product more than once. Please choose unique products.")
    #                     return render(request, 'sales/sale_form.html', {
    #                         'form': form,
    #                         'saleproduct_formset': saleproduct_formset,
    #                         'customers': Customer.objects.all(),
    #                         'products': Product.objects.all()
    #                     })
    #
    #                 products.append(product)
    #                 total_price += product.price * quantity
    #                 total_profit += (product.high_price - product.price) * quantity
    #
    #                 sale_product = sale_product_form.save(commit=False)
    #                 sale_product.sale = sale
    #                 sale_product.save()  # Guardar el producto de la venta
    #
    #                 product.sold_quantity += quantity
    #                 product.save()
    #
    #         sale.total_price = total_price
    #         sale.total_profit = total_profit
    #         sale.save()
    #
    #         messages.success(request, "Sale was created successfully!")
    #         return redirect('sales:sale_list')
    #     else:
    #         if form.errors:
    #             print("SaleForm errors:", form.errors)
    #         if saleproduct_formset.errors:
    #             print("SaleProductFormSet errors:", saleproduct_formset.errors)
    #         messages.error(request, "There was an error creating the sale. Please try again.")
    # else:
    #     form = SaleForm()
    #     saleproduct_formset = saleproductformset()
    #
    # return render(request, 'sales/sale_form.html', {
    #     'form': form,
    #     'saleproduct_formset': saleproduct_formset,
    #     'customers': Customer.objects.all(),
    #     'products': Product.objects.all(),
    # })
