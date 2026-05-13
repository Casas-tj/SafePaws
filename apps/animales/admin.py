from django.contrib import admin
from .models import Animal


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'breed', 'age_years', 'age_months',
                    'sex', 'vaccinated', 'sterilized', 'owner', 'is_active']
    list_filter = ['species', 'sex', 'vaccinated', 'sterilized', 'is_active']
    search_fields = ['name', 'breed']
