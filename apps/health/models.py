from django.db import models
from apps.core.models import TimeStampedModel
from apps.animales.models import Animal


class MedicalEvent(TimeStampedModel):

    TYPE_CHOICES = [
        ('Emergencia', 'Emergencia'),
        ('Consulta', 'Consulta'),
        ('Control', 'Control'),
        ('Procedimiento', 'Procedimiento'),
        ('Otro', 'Otro'),
    ]

    SEVERITY_CHOICES = [
        ('Alta', 'Alta'),
        ('Media', 'Media'),
        ('Baja', 'Baja'),
    ]

    STATUS_CHOICES = [
        ('Abierto', 'Abierto'),
        ('En Proceso', 'En Proceso'),
        ('Resolved', 'Resuelto'),
    ]

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='medical_events',
        verbose_name='Animal'
    )

    event_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        verbose_name='Tipo de atención'
    )

    description = models.TextField(
        verbose_name='Descripción'
    )

    incident_date = models.DateField(
        verbose_name='Fecha de la atención'
    )

    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='Media',
        verbose_name='Severidad'
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='Abierto',
        verbose_name='Estado'
    )

    resolved_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de resolución'
    )

    def __str__(self):
        return f"{self.event_type} — {self.animal.name} ({self.incident_date})"

    class Meta:
        verbose_name = 'Evento Médico'
        verbose_name_plural = 'Eventos Médicos'
        ordering = ['-incident_date']
