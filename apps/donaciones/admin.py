from django.contrib import admin
from .models import Donacion


@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display = ['donante', 'donation_type',
                    'status', 'amount', 'payment_method', 'date']
    list_filter = ['donation_type', 'status', 'payment_method']
    search_fields = ['donante', 'donante_email', 'description']
    date_hierarchy = 'date'
    ordering = ['-date']
