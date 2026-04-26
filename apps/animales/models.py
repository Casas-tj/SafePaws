from django.db import models


class Animal(models.Model):

    ESPECIE_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Conejo', 'Conejo'),
        ('Hamster', 'Hamster'),
        ('Pajaro', 'Pájaro'),
        ('Otro', 'Otro'),
    ]

    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Hembra', 'Hembra'),
    ]

    ESTADO_CHOICES = [
        ('En Adopcion', 'En Adopción'),
        ('En Acogida', 'En Acogida'),
        ('Adoptado', 'Adoptado'),
        ('Fallecido', 'Fallecido'),
    ]

    VACUNADO_CHOICES = [
        ('Si', 'Sí'),
        ('No', 'No'),
        ('Parcialmente', 'Parcialmente'),
    ]

    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50, choices=ESPECIE_CHOICES)
    raza = models.CharField(max_length=100, blank=True)
    edad = models.CharField(max_length=50, blank=True)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, blank=True)
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='En Adopcion'
    )
    fecha_ingreso = models.DateField()
    vacunado = models.CharField(
        max_length=15, choices=VACUNADO_CHOICES, blank=True
    )
    esterilizado = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.especie})"

    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animales'
        ordering = ['-created_at']
