from django.urls import path
from . import views

urlpatterns = [

    # SUMINISTROS
    path('suministros', views.suministros, name='suministros'),

    # INVENTARIO — Productos
    path('inventario', views.inventario, name='inventario'),
    path('inventario_form/', views.inventario_form, name='inventario_form'),
    path('inventario_form/<int:product_id>/',
         views.inventario_form, name='inventario_form_edit'),
    path('inventario_delete/<int:product_id>/',
         views.inventario_delete, name='inventario_delete'),
    path('inventario_details/<int:product_id>/',
         views.inventario_details, name='inventario_details'),

    # STOCK — Movimientos
    path('stock', views.stock, name='stock'),
    path('stock_form/', views.stock_form, name='stock_form'),
    path('stock_form/<int:movement_id>/',
         views.stock_form, name='stock_form_edit'),
    path('stock_delete/<int:movement_id>/',
         views.stock_delete, name='stock_delete'),
    path('stock_details/<int:movement_id>/',
         views.stock_details, name='stock_details'),
]
