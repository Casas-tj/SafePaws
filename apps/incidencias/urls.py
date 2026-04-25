from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('incidencias', views.incidencias, name="incidencias"),
    path('incidencias_form',
         views.incidencias_form, name="incidencias_form"),
]
