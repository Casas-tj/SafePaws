from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventario/suministros', views.suministros, name="suministros"),
    path('inventario/inventario',
         views.inventario, name="inventario"),
    path('inventario/stock',
         views.stock, name="stock"),
]
