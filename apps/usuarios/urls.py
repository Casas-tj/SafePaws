from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/usuarios', views.usuarios, name="usuarios"),
    path('usuarios/usuarios_form',
         views.usuarios_form, name="usuarios_form"),
    path('usuarios/roles',
         views.roles, name="roles"),
    path('usuarios/roles_form',
         views.roles_form, name="roles_form"),
    path('usuarios/recuperar_contrasena',
         views.recuperar_contrasena, name="recuperar_contrasena"),
]
