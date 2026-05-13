from django.contrib import admin
from .models import Owner


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'email', 'phone', 'is_volunteer']
    search_fields = ['name', 'last_name', 'email']
