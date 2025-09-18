# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem, OrderShippingInfo

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","user","status","total","created_at")
    inlines = [OrderItemInline]

@admin.register(OrderShippingInfo)
class OrderShippingInfoAdmin(admin.ModelAdmin):
    list_display = ("order", "full_name", "email", "city")