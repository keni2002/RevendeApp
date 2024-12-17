from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


@login_required
def customer_list(request):
    query = request.GET.get('q', '')
    customer_list = Customer.objects.filter(user=request.user)

    if query:
        customer_list = customer_list.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        ).distinct()

    items_per_page = request.GET.get('items_per_page', 5)

    order_by = request.GET.get('order_by', 'created')
    ordering = request.GET.get('ordering', 'desc')
    valid_order_fields = ['name', 'phone', 'email', 'created', 'updated']

    if order_by not in valid_order_fields:
        order_by = 'name'

    if ordering == 'desc':
        order_by = f'-{order_by}'

    customer_list = customer_list.order_by(order_by)

    paginator = Paginator(customer_list, items_per_page)

    page_number = request.GET.get('page', 1)
    try:
        customers = paginator.page(page_number)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    return render(request, 'customers/customer_list.html', {
        'customers': customers,
        'items_per_page': items_per_page,
        'order_by': order_by.lstrip('-'),
        'ordering': 'desc' if order_by.startswith('-') else 'asc',
        'query': query,
        'section': 'customers'
    })


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'

class CustomerCreateView(SuccessMessageMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer:customer_list')
    success_message = "Customer wa  s created successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the customer. Please try again.")
        return self.render_to_response(self.get_context_data(form=form))

class CustomerUpdateView(SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer:customer_list')
    success_message = "Customer was updated successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the customer. Please try again.")
        return self.render_to_response(self.get_context_data(form=form))

class CustomerDeleteView(SuccessMessageMixin, DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customer:customer_list')
    success_message = "Customer was deleted successfully!"
