from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('animales/animales', views.animales, name="animales"),
    path('animales/animales_form',
         views.animales_form, name="animales_form"),
]
