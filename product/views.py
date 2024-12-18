from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from .models import Product
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import DetailView
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import F, DecimalField, Value as V
from django.db.models import F, ExpressionWrapper, DecimalField, Value as V
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ProductForm

# Create your views here.
@login_required
def product_list(request, categories_slug=None):
    query = request.GET.get('q', '')
    product_list = Product.objects.filter(retailer=request.user)
    category = None

    if categories_slug:
        category = get_object_or_404(Tag, slug=categories_slug)
        product_list = product_list.filter(categories__in=[category])


    if query:
        product_list = product_list.filter(
            Q(name__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()


    items_per_page = request.GET.get('items_per_page', 5)


    product_list = product_list.annotate(
        cost=ExpressionWrapper(
            F('price') * F('quantity'),
            output_field=DecimalField()
        ),
        expected_profit=ExpressionWrapper(
            (F('high_price') - F('price')) * F('quantity'),
            output_field=DecimalField()
        ),
        price_cup=ExpressionWrapper(
            F('price') *
            (F('currency') == 'USD' and settings.USD_TO_CUP or
             F('currency') == 'MLC' and settings.MLC_TO_CUP or 1),
            output_field=DecimalField()
        )
    )


    order_by = request.GET.get('order_by', 'created')
    ordering = request.GET.get('ordering', 'desc')
    valid_order_fields = ['name', 'price', 'high_price', 'currency', 'quantity', 'expected_profit', 'cost', 'created', 'updated']

    if order_by not in valid_order_fields:
        order_by = 'name'

    if ordering == 'desc':
        order_by = f'-{order_by}'

    product_list = product_list.order_by(order_by)

    paginator = Paginator(product_list, items_per_page)

    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'products/product_list.html', {
        'products': products,
        'category': category,
        'items_per_page': items_per_page,
        'order_by': order_by.lstrip('-'),
        'ordering': 'desc' if order_by.startswith('-') else 'asc',
        'query': query,
        'section': 'products'
    })


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'



class ProductCreateView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_add.html'
    success_url = reverse_lazy('product:products')
    success_message = "Product was created successfully!"

    def form_valid(self, form):
        form.instance.retailer = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the product. Please try again.")
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_edit.html'
    success_url = reverse_lazy('product:products')
    success_message = "Product was updated successfully!"

    def form_valid(self, form):
        form.instance.retailer = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the product. Please try again.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = self.object.categories.all()
        context['formatted_categories'] = ', '.join([tag.name for tag in categories])
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_delete.html'
    success_url = reverse_lazy('product:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_name'] = self.get_object().name
        return context

    def form_valid(self, form):
        messages.success(self.request, "Product deleted successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error deleting product')
        return super().form_invalid(form)


