from django.db import models


class Donacion(models.Model):

    TIPO_CHOICES = [
        ('Monetaria', 'Monetaria'),
        ('Material', 'Material'),
        ('Otra', 'Otro tipo'),
    ]

    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Recibida', 'Recibida'),
        ('Procesada', 'Procesada'),
        ('Cancelada', 'Cancelada'),
    ]

    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Tarjeta', 'Tarjeta'),
        ('Cheque', 'Cheque'),
        ('PayPal', 'PayPal'),
        ('Otro', 'Otro'),
    ]

    # Datos del donante
    donante = models.CharField(
        max_length=200,
        help_text="Nombre del donante o 'Anónimo'"
    )
    donante_email = models.EmailField(blank=True, verbose_name='Email')
    donante_telefono = models.CharField(
        max_length=20, blank=True, verbose_name='Teléfono'
    )

    # Detalles de la donación
    fecha = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(
        max_length=15, choices=ESTADO_CHOICES, default='Pendiente'
    )

    # Solo para donaciones monetarias
    monto = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        verbose_name='Monto (€)'
    )
    metodo_pago = models.CharField(
        max_length=20, choices=METODO_PAGO_CHOICES,
        blank=True, verbose_name='Método de pago'
    )

    descripcion = models.TextField(
        blank=True,
        help_text='Materiales donados, concepto del pago...'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo} — {self.donante} ({self.fecha})"

    class Meta:
        verbose_name = 'Donación'
        verbose_name_plural = 'Donaciones'
        ordering = ['-fecha']
