from django.contrib import admin
from .models import Product
# Register your models here.

@admin.register(Product)
class ProductForm(admin.ModelAdmin):
     list_display = ['name', 'retailer', 'price', 'high_price', 'quantity', 'currency', 'unit']
     raw_id_fields = ['retailer']
     exclude = ['sold_quantity']

