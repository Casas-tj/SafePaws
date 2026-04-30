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

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, choices=ESPECIE_CHOICES)
    breed = models.CharField(max_length=100, blank=True)
    age = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=10, choices=SEXO_CHOICES, blank=True)
    status = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='En Adopcion'
    )
    admission_date = models.DateField()
    vaccinated = models.CharField(
        max_length=15, choices=VACUNADO_CHOICES, blank=True
    )
    spayed = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.species})"

    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animales'
        ordering = ['-created_at']
