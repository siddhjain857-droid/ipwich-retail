# catalog/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("products/<int:pk>/", views.detail, name="product_detail"),
]
