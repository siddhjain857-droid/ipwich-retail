# catalog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    cat = request.GET.get("category")
    qs = Product.objects.all().order_by("-created_at")
    if cat: qs = qs.filter(category__name__iexact=cat)
    cats = Category.objects.all()
    return render(request, "catalog/home.html", {"products": qs, "categories": cats, "active": cat})

def detail(request, pk):
    p = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/detail.html", {"product": p})
