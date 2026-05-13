from django.db import models
from apps.core.models import TimeStampedModel
from apps.animales.models import Animal
from apps.owners.models import Owner


class Adopcion(TimeStampedModel):

    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aprobada', 'Aprobada'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]

    animal = models.ForeignKey(
        Animal,
        on_delete=models.PROTECT,
        related_name='adopciones'
    )

    owner = models.ForeignKey(
        Owner,
        on_delete=models.PROTECT,
        related_name='adopciones'
    )

    adoption_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendiente')

    def __str__(self):
        return f"{self.animal} → {self.owner} ({self.adoption_date})"

    class Meta:
        verbose_name = 'Adopción'
        verbose_name_plural = 'Adopciones'
        ordering = ['-created_at']
