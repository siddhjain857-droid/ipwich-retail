# catalog/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self): return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products",
                                 on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name
    @property
    def in_stock(self): return self.stock > 0