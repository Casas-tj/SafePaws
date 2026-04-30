from django.db import models

from apps.animales.models import Animal


class Adopcion(models.Model):

    ESTADO_CHOICES = [
        ('En Proceso', 'En Proceso'),
        ('Aprobada', 'Aprobada'),
        ('Completada', 'Completada'),
        ('Rechazada', 'Rechazada'),
    ]

    # Relación con el animal
    animal = models.ForeignKey(
        Animal,
        on_delete=models.PROTECT,
        related_name='adopciones',
        verbose_name='Animal'
    )

    # Estado del proceso de adopción
    status = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='En Proceso'
    )
    fecha_solicitud = models.DateField()
    fecha_adopcion = models.DateField(null=True, blank=True)

    # Datos del adoptante (en el mismo formulario, como en el template)
    adoptante_nombre = models.CharField(
        max_length=200, verbose_name='Nombre del adoptante')
    adoptante_telefono = models.CharField(
        max_length=20, verbose_name='Teléfono')
    adoptante_email = models.EmailField(verbose_name='Email')
    adoptante_direccion = models.CharField(
        max_length=300, blank=True, verbose_name='Dirección')

    # Observaciones
    observaciones = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.animal} → {self.adoptante_nombre} ({self.estado})"

    class Meta:
        verbose_name = 'Adopción'
        verbose_name_plural = 'Adopciones'
        ordering = ['-created_at']
