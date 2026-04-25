from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('donaciones', views.donaciones, name="donaciones"),
    path('donaciones_form',
         views.donaciones_form, name="donaciones_form"),
]
