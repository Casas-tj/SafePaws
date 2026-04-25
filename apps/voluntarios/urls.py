from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   
    path('voluntarios', views.voluntarios, name="voluntarios"),
    path('voluntarios_form',
         views.voluntarios_form, name="voluntarios_form"),
    
]
