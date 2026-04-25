from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('suministros', views.suministros, name="suministros"),
    path('inventario',
         views.inventario, name="inventario"),
    path('stock',
         views.stock, name="stock"),
]
