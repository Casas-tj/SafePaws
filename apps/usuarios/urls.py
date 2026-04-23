from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('usuarios', views.usuarios, name="usuarios"),
    path('usuarios_form',
         views.usuarios_form, name="usuarios_form"),
    path('roles',
         views.roles, name="roles"),
    path('recuperar_contrasena',
         views.recuperar_contrasena, name="recuperar_contrasena"),
]
