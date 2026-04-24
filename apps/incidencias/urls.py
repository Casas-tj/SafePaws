from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('incidencias/incidencias', views.incidencias, name="incidencias"),
    path('incidencias/incidencias_form',
         views.incidencias_form, name="incidencias_form"),
]
