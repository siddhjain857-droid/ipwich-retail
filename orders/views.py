# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from catalog.models import Product
from .models import Order, OrderItem

CART_KEY = "cart"

@login_required
def checkout(request):
    cart = request.session.get(CART_KEY, {})
    if not cart: return redirect("cart")
    items, total = [], Decimal("0.00")
    for pid, qty in cart.items():
        prod = Product.objects.get(pk=int(pid))
        items.append((prod, qty))
        total += prod.price * qty
    if request.method == "POST":
        order = Order.objects.create(user=request.user, total=total, status="pending")
        for prod, qty in items:
            OrderItem.objects.create(order=order, product=prod, quantity=qty, price_each=prod.price)
            # decrement stock
            prod.stock = max(0, prod.stock - qty)
            prod.save(update_fields=["stock"])
        request.session[CART_KEY] = {}
        return redirect("order_confirmation", order_id=order.id)
    return render(request, "orders/checkout.html", {"items": items, "total": total})

@login_required
def confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, "orders/confirmation.html", {"order": order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/list.html", {"orders": orders})
