from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('adopciones', views.adopciones, name="adopciones"),
    path('adopciones_form',
         views.adopciones_form, name="adopciones_form"),
]
