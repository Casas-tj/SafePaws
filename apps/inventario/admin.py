from django.contrib import admin
from .models import Product, Movement


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'unit', 'is_active']
    list_filter = ['unit', 'is_active']
    search_fields = ['name', 'description']


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'type', 'quantity', 'movement_date']
    list_filter = ['type', 'movement_date']
    search_fields = ['product__name', 'reason']
    date_hierarchy = 'movement_date'
