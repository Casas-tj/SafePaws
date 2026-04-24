from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adopciones/adopciones', views.adopciones, name="adopciones"),
    path('adopciones/adopciones_form',
         views.adopciones_form, name="adopciones_form"),
]
