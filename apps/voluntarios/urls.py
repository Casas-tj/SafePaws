from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('voluntarios/voluntarios', views.voluntarios, name="voluntarios"),
    path('voluntarios/voluntarios_form',
         views.voluntarios_form, name="voluntarios_form"),
    path('voluntarios/funciones', views.funciones, name="funciones"),
]
