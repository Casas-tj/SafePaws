from django.urls import path
from . import views

urlpatterns = [
    path('', views.reportes, name="reportes"),
    path('reporte_adopciones', views.reporte_adopciones, name="reporte_adopciones"),
    path('reporte_inventario', views.reporte_inventario, name="reporte_inventario"),
]
