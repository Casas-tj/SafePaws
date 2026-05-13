from django.contrib import admin
from .models import MedicalEvent


@admin.register(MedicalEvent)
class MedicalEventAdmin(admin.ModelAdmin):
    list_display = ['animal', 'event_type', 'incident_date', 'description']
    list_filter = ['event_type']
