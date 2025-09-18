# cart/views.py
from django.shortcuts import redirect, render, get_object_or_404
from catalog.models import Product
from decimal import Decimal

CART_KEY = "cart"

def add_to_cart(request, product_id):
    p = get_object_or_404(Product, pk=product_id)
    qty = int(request.POST.get("qty", 1))
    cart = request.session.get(CART_KEY, {})
    cart[str(p.id)] = cart.get(str(p.id), 0) + qty
    request.session[CART_KEY] = cart
    return redirect("cart")

def remove_from_cart(request, product_id):
    cart = request.session.get(CART_KEY, {})
    cart.pop(str(product_id), None)
    request.session[CART_KEY] = cart
    return redirect("cart")

def clear_cart(request):
    request.session[CART_KEY] = {}
    return redirect("cart")

def view_cart(request):
    cart = request.session.get(CART_KEY, {})
    items, total = [], Decimal("0.00")
    for pid, qty in cart.items():
        prod = get_object_or_404(Product, pk=int(pid))
        line = {"product": prod, "qty": qty, "line_total": prod.price * qty}
        total += line["line_total"]
        items.append(line)
    return render(request, "cart/cart.html", {"items": items, "total": total})

def update_cart(request, product_id):  # optional, if you want quantity update on the cart page
    qty = max(1, int(request.POST.get("qty", 1)))
    cart = request.session.get(CART_KEY, {})
    if str(product_id) in cart:
        cart[str(product_id)] = qty
    request.session[CART_KEY] = cart
    return redirect("cart")