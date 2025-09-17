# orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("confirmation/<int:order_id>/", views.confirmation, name="order_confirmation"),
    path("", views.my_orders, name="my_orders"),
]
