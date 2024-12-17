from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=18, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers',default=None)

    def __str__(self):
        return self.name
