from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=18, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
