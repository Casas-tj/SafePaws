from django.contrib import admin
from .models import Adopcion


@admin.register(Adopcion)
class AdopcionAdmin(admin.ModelAdmin):
    list_display = ['animal', 'owner',
                    'adoption_date', 'is_active', 'created_at']
    list_filter = ['is_active', 'adoption_date']
    search_fields = ['animal__name', 'owner__name', 'owner__last_name']
    date_hierarchy = 'adoption_date'
    ordering = ['-created_at']
