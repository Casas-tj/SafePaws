from django.db import models


class Voluntario(models.Model):

    ROL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Coordinador', 'Coordinador'),
        ('Veterinario', 'Veterinario'),
        ('Cuidador', 'Cuidador'),
        ('Adiestrador', 'Adiestrador'),
        ('Rescatista', 'Rescatista'),
        ('Redes Sociales', 'Redes Sociales'),
    ]

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    info_adicional = models.TextField(
        blank=True,
        verbose_name='Información adicional',
        help_text='Experiencia, disponibilidad, habilidades...'
    )
    activo = models.BooleanField(default=True)
    fecha_alta = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.rol})"

    class Meta:
        verbose_name = 'Voluntario'
        verbose_name_plural = 'Voluntarios'
        ordering = ['apellidos', 'nombre']
