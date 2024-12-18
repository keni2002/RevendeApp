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
from .forms import SaleForm, SaleProductFormSet
from customer.models import Customer
from product.models import Product


@login_required
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        saleproduct_formset = SaleProductFormSet(request.POST)

        if form.is_valid() and saleproduct_formset.is_valid():
            sale = form.save(commit=False)
            sale.total_profit = 0
            sale.total_price = 0
            sale.user = request.user
            sale.save()

            products = []
            for sale_product_form in saleproduct_formset:
                if sale_product_form.cleaned_data:
                    product = sale_product_form.cleaned_data['product']
                    quantity = sale_product_form.cleaned_data['quantity']
                    if product in products:
                        messages.error(request,
                                       "You have selected the same product more than once. Please choose unique products.")
                        return render(request, 'sales/sale_form.html', {
                            'form': form,
                            'saleproduct_formset': saleproduct_formset,
                            'customers': Customer.objects.all(),
                            'products': Product.objects.all()
                        })
                    products.append(product)

            saleproduct_formset.instance = sale
            saleproduct_formset.save()

            # Actualizar sold_quantity en cada producto
            total_price = 0
            total_profit = 0
            for sale_product_form in saleproduct_formset:
                if sale_product_form.cleaned_data:
                    product = sale_product_form.cleaned_data['product']
                    quantity = sale_product_form.cleaned_data['quantity']
                    product.sold_quantity += quantity
                    product.save()
                    total_price += sale_product_form.instance.total_price
                    total_profit += sale_product_form.instance.total_profit

            sale.total_price = total_price
            sale.total_profit = total_profit
            sale.save()

            messages.success(request, "Sale was created successfully!")
            return redirect('sales:sale_list')
        else:
            messages.error(request, "There was an error creating the sale. Please try again.")
    else:
        form = SaleForm()
        saleproduct_formset = SaleProductFormSet()

    return render(request, 'sales/sale_form.html', {
        'form': form,
        'saleproduct_formset': saleproduct_formset,
        'customers': Customer.objects.all(),
        'products': Product.objects.all(),
    })
