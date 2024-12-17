from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.

class Product(models.Model):
    class Status(models.TextChoices):
        CUP = 'CUP','CUP'
        USD = 'USD','USD'
        MLC = 'MLC','MLC'
    name = models.CharField(max_length=100)
    retailer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    sold_quantity = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=10, choices=Status.choices, default=Status.CUP)
    unit = models.CharField(max_length=50,default='unit')
    categories = TaggableManager(verbose_name='Categories', blank=True)
    #time
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def expected_profit(self):
        return (self.high_price - self.price) * self.quantity

    def investment(self):
        return self.price * self.quantity

    def potential_profit(self):
        return (self.high_price - self.price) * (self.quantity - self.sold_quantity)

    def profit_so_far(self):
        return (self.high_price - self.price) * self.sold_quantity

    def remaining_stock(self):
        return self.quantity - self.sold_quantity

    def progress_percent(self):
        return (self.sold_quantity / self.quantity) * 100 if self.quantity > 0 else 0

    class Meta:
        ordering = ['-created']
        # provide index, improve performance for queries filtering
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name




