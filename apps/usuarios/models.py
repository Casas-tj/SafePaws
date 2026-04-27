from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    #Campos
    telefono = models.CharField(max_length=20, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.username