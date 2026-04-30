from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('animales', views.animales, name="animales"),

    # 🆕 Crear animal
    path('animales_form',
         views.animales_form, name="animales_form"),

    # ✏️ Editar animal
    path('animales_form/<int:animal_id>/',
         views.animales_form, name="animales_form_edit"),

    # Eliminar animal
    path('animales_delete/<int:animal_id>/',
         views.animales_delete, name="animales_delete"),
]
