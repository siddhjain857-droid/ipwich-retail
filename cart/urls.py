# cart/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='cart_add'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='cart_remove'),
    path('clear/', views.clear_cart, name='cart_clear'),
    path("update/<int:product_id>/", views.update_cart, name="update_cart"),
]
