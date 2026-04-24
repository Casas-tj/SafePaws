from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/home', views.home, name="home"),
    path('dashboard/dashboard', views.dashboard, name="dashboard"),
]
