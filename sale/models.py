from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
from product.models import Product
from django.conf import settings

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales')
    products = models.ManyToManyField(Product, through='SaleProduct')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale to {self.customer.name} on {self.created}"

class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def convert_to_cup(self, amount, currency):
        if currency == 'USD':
            return amount * settings.USD_TO_CUP
        elif currency == 'MLC':
            return amount * settings.MLC_TO_CUP
        return amount

    @property
    def total_price(self):
        return self.convert_to_cup(self.product.price, self.product.currency) * self.quantity

    @property
    def total_profit(self):
        return self.convert_to_cup(self.product.high_price - self.product.price, self.product.currency) * self.quantity
