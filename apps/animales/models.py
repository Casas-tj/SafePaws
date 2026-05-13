from django.db import models
from apps.core.models import TimeStampedModel


class Animal(TimeStampedModel):

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

    STATUS_CHOICES = [
        ('Disponible', 'Disponible'),
        ('En Tratamiento', 'En Tratamiento'),
        ('Sano', 'Sano'),
        ('Critico', 'Crítico'),
        ('Adoptado', 'Adoptado'),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, choices=ESPECIE_CHOICES)
    breed = models.CharField(max_length=100, blank=True)
    age_years = models.PositiveIntegerField(null=True, blank=True, default=0)
    age_months = models.PositiveIntegerField(null=True, blank=True, default=0)
    sex = models.CharField(max_length=10, choices=SEXO_CHOICES, blank=True)
    admission_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponible')
    vaccinated = models.BooleanField(default=False)
    sterilized = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        'owners.Owner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='animals'
    )

    def __str__(self):
        return f"{self.name} ({self.species})"

    @property
    def age_display(self):
        y = self.age_years or 0
        m = self.age_months or 0

        if y == 0 and m == 0:
            return "-"
        elif y > 0 and m > 0:
            return f"{y} año(s) y {m} mes(es)"
        elif y > 0:
            return f"{y} año(s)"
        else:
            return f"{m} mes(es)"

    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animales'
        ordering = ['-created_at']
