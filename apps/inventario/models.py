from django.db import models
from apps.core.models import TimeStampedModel


class Product(TimeStampedModel):

    UNIT_CHOICES = [
        ('kg', 'Kilogramos'),
        ('g', 'Gramos'),
        ('L', 'Litros'),
        ('ml', 'Mililitros'),
        ('ud', 'Unidades'),
        ('caja', 'Cajas'),
        ('bolsa', 'Bolsas'),
    ]

    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    quantity = models.IntegerField(default=0, verbose_name='Stock actual')

    unit = models.CharField(
        max_length=20, choices=UNIT_CHOICES,
        blank=True, verbose_name='Unidad de medida'
    )

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['name']


class Movement(TimeStampedModel):

    TYPE_CHOICES = [
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
    ]

    product = models.ForeignKey(
        Product,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='movements',
        verbose_name='Producto principal'
    )

    movement_date = models.DateField(verbose_name='Fecha del movimiento')
    quantity = models.IntegerField(
        default=0, verbose_name='Cantidad (producto principal)')
    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES,
        verbose_name='Tipo de movimiento'
    )
    reason = models.TextField(
        blank=True, verbose_name='Motivo / Observaciones')

    def __str__(self):
        product_name = self.product.name if self.product else "Multi-producto"
        return f"{self.type} — {product_name} ({self.movement_date})"

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['-movement_date']
