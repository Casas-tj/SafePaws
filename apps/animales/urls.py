from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('animales', views.animales, name="animales"),
    path('animales_form',
         views.animales_form, name="animales_form"),
]
