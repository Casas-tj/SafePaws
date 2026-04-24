from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('donaciones/donaciones', views.donaciones, name="donaciones"),
    path('donaciones/donaciones_form',
         views.donaciones_form, name="donaciones_form"),
]
