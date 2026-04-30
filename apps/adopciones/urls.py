from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('adopciones', views.adopciones, name="adopciones"),

    # 🆕 Crear animal
    path('adopciones_form',
         views.adopciones_form, name="adopciones_form"),

    # ✏️ Editar animal
    path('adopciones_form/<int:adopcion_id>/',
         views.adopciones_form, name="adopciones_form_edit"),

    # Eliminar animal
    path('adopciones_delete/<int:adopcion_id>/',
         views.adopciones_delete, name="adopciones_delete"),
]

