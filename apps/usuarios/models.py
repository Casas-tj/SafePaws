from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Usuario(models.Model):
    usuario = models.CharField(
        max_length=30, blank=False, null=False, unique=True)
    contrasena = models.CharField(max_length=20, blank=False, null=False)
    categoria = models.CharField(max_length=30, blank=False, null=False)
    #nombre = models.CharField(max_length=30, blank=False, null=False)
    #apellido = models.CharField(max_length=30, blank=False, null=False)
    telefono = models.CharField(
        max_length=15, blank=False, null=False),
    #email = models.EmailField(unique=True)
    #direccion = models.CharField(max_length=30, null=False)
    ciudad = models.CharField(max_length=30, blank=False, null=False)
    codigo_postal = models.CharField(
        max_length=10, blank=False, null=False)
    #evaluar estado con choices
    #activo = models.BooleanField(default=True)
    verificado = models.BooleanField(default=False)
    ultimo_acceso = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
