from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
     path('', views.usuarios, name="usuarios"),
    # 🆕 Crear usuario
     path('usuarios_form/', views.usuarios_form, name="usuarios_form"),
    # ✏️ Editar usuario
     path('usuarios_form/<int:user_id>/', views.usuarios_form, name="usuarios_form_edit"),
     #Eliminar usuario
     path('usuarios_delete/<int:user_id>/', views.usuarios_delete, name="usuarios_delete"),

     path('roles/', views.roles, name="roles"),
     path('roles_form/', views.roles_form, name="roles_form"),
     path('recuperar_contrasena/', views.recuperar_contrasena, name="recuperar_contrasena"),
]
