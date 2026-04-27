from django.db import models


class Suministro(models.Model):
    """Catálogo de productos del almacén."""

    nombre = models.CharField(
        max_length=200, verbose_name='Nombre del artículo'
    )
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(
        default=5, verbose_name='Stock mínimo'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def stock_bajo(self):
        """True si el stock actual está por debajo del mínimo."""
        return self.stock <= self.stock_minimo

    @property
    def estado_stock(self):
        if self.stock == 0:
            return 'Sin stock'
        if self.stock_bajo:
            return 'Stock bajo'
        return 'OK'

    def __str__(self):
        return f"{self.nombre} (stock: {self.stock})"

    class Meta:
        verbose_name = 'Suministro'
        verbose_name_plural = 'Suministros'
        ordering = ['nombre']


class MovimientoStock(models.Model):
    """Historial de entradas y salidas de cada producto."""

    TIPO_CHOICES = [
        ('Entrada', 'Entrada (+)'),
        ('Salida', 'Salida (-)'),
    ]

    suministro = models.ForeignKey(
        Suministro,
        on_delete=models.CASCADE,
        related_name='movimientos'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.tipo} {self.cantidad} × {self.suministro.nombre}"

    class Meta:
        verbose_name = 'Movimiento de stock'
        verbose_name_plural = 'Movimientos de stock'
        ordering = ['-fecha']
