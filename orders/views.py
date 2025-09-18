# # orders/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from decimal import Decimal
# from catalog.models import Product
# from .models import Order, OrderItem, OrderShippingInfo
# from django.db import transaction
# from .forms import CheckoutForm

# CART_KEY = "cart"

# @login_required
# def checkout(request):
#     cart = request.session.get(CART_KEY, {})
#     if not cart: 
#         return redirect("cart")
    
#     items = []
#     total = Decimal("0.00")
#     for pid, qty in cart.items():
#         qty = max(1, int(qty))
#         prod = get_object_or_404(Product, pk=int(pid))
#         line_total = prod.price * qty
#         items.append({"product": prod, "qty": qty, "line_total": line_total})
#         total += line_total

#     if request.method == "POST":
#         # All-or-nothing: create order + items + stock decrement atomically
#         with transaction.atomic():
#             order = Order.objects.create(
#                 user=request.user,
#                 total=Decimal("0.00"),   # set after we add items
#                 status="pending",
#             )

#             running_total = Decimal("0.00")

#             for row in items:
#                 p = row["product"]
#                 qty = row["qty"]

#                 OrderItem.objects.create(
#                     order=order,
#                     product=p,
#                     quantity=qty,
#                     price_each=p.price,
#                 )
#                 running_total += p.price * qty

#                 # Decrement stock (don’t go negative)
#                 p.stock = max(0, p.stock - qty)
#                 p.save(update_fields=["stock"])

#             # Finalize order total
#             order.total = running_total
#             order.save(update_fields=["total"])

#             # Clear cart
#             request.session[CART_KEY] = {}

#         return redirect("order_confirmation", order_id=order.id)

#     return render(request, "orders/checkout.html", {"items": items, "total": total})

# @login_required
# def confirmation(request, order_id):
#     order = get_object_or_404(Order, pk=order_id, user=request.user)
#     return render(request, "orders/confirmation.html", {"order": order})

# @login_required
# def my_orders(request):
#     orders = Order.objects.filter(user=request.user).order_by("-created_at")
#     return render(request, "orders/list.html", {"orders": orders})

# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal

from catalog.models import Product
from .models import Order, OrderItem, OrderShippingInfo
from .forms import CheckoutForm

CART_KEY = "cart"

@login_required
def checkout(request):
    cart = request.session.get(CART_KEY, {})
    if not cart:
        return redirect("cart")

    # Build items + total for summary
    items = []
    total = Decimal("0.00")
    for pid, qty in cart.items():
        qty = max(1, int(qty))
        prod = get_object_or_404(Product, pk=int(pid))
        line_total = prod.price * qty
        items.append({"product": prod, "qty": qty, "line_total": line_total})
        total += line_total

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create order shell
                order = Order.objects.create(
                    user=request.user,
                    total=Decimal("0.00"),
                    status="pending",
                )

                # Persist shipping/contact data
                OrderShippingInfo.objects.create(
                    order=order,
                    **form.cleaned_data,
                )

                # Create order items + decrement stock + compute total
                running_total = Decimal("0.00")
                for row in items:
                    p = row["product"]
                    qty = row["qty"]

                    OrderItem.objects.create(
                        order=order,
                        product=p,
                        quantity=qty,
                        price_each=p.price,
                    )
                    running_total += p.price * qty

                    p.stock = max(0, p.stock - qty)
                    p.save(update_fields=["stock"])

                # Finalize order total
                order.total = running_total
                order.save(update_fields=["total"])

                # Clear cart
                request.session[CART_KEY] = {}

            return redirect("order_confirmation", order_id=order.id)
        else:
            # Invalid form → fall through and re-render with errors
            pass
    else:
        form = CheckoutForm()

    return render(
        request,
        "orders/checkout.html",
        {"form": form, "items": items, "total": total},
    )


@login_required
def confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, "orders/confirmation.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/list.html", {"orders": orders})