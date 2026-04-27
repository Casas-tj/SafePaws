from django.db import models

from apps.animales.models import Animal


class Incidencia(models.Model):

    CATEGORIA_CHOICES = [
        ('Mantenimiento', 'Mantenimiento'),
        ('Salud', 'Salud'),
        ('Comportamiento', 'Comportamiento'),
        ('Suministros', 'Suministros'),
        ('Sistema', 'Sistema'),
        ('Seguridad', 'Seguridad'),
        ('Limpieza', 'Limpieza'),
        ('Otro', 'Otro'),
    ]

    PRIORIDAD_CHOICES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta (Urgente)'),
        ('Critica', 'Crítica (Atención Inmediata)'),
    ]

    ESTADO_CHOICES = [
        ('Abierta', 'Abierta'),
        ('En Proceso', 'En Proceso'),
        ('Resuelta', 'Resuelta'),
        ('Cerrada', 'Cerrada'),
    ]

    # Animal relacionado (opcional: no todas las incidencias afectan a un animal)
    animal = models.ForeignKey(
        Animal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidencias',
        verbose_name='Animal relacionado'
    )

    titulo = models.CharField(max_length=200, verbose_name='Asunto / Título')
    categoria = models.CharField(
        max_length=30, choices=CATEGORIA_CHOICES, verbose_name='Tipo de incidencia'
    )
    ubicacion = models.CharField(max_length=200, verbose_name='Ubicación')
    prioridad = models.CharField(
        max_length=10, choices=PRIORIDAD_CHOICES, default='Media'
    )
    estado = models.CharField(
        max_length=15, choices=ESTADO_CHOICES, default='Abierta'
    )
    descripcion = models.TextField(verbose_name='Descripción detallada')
    fecha_reporte = models.DateField(verbose_name='Fecha de reporte')
    fecha_resolucion = models.DateField(
        null=True, blank=True, verbose_name='Fecha de resolución'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.categoria}] {self.titulo} — {self.estado}"

    class Meta:
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'
        ordering = ['-fecha_reporte', '-created_at']
