from django.contrib import admin

from .models import SaleProduct,Sale

# Register your models here.
admin.site.register(Sale)
admin.site.register(SaleProduct)