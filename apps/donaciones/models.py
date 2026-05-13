from django.db import models
from apps.core.models import TimeStampedModel


class Donacion(TimeStampedModel):

    """
    Gestión de donaciones al refugio SafePaws.

    Esta app no forma parte del MER principal del sistema de gestión
    de animales, pero se incluye como funcionalidad adicional para dar
    soporte a la operativa económica del refugio.

    Tipos soportados: monetarias (con monto y método de pago) y materiales.
    Estados: Pendiente → Recibida → Procesada | Cancelada.
    """

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

    donante = models.CharField(
        max_length=200,
        help_text="Nombre del donante o 'Anónimo'"
    )
    donante_email = models.EmailField(blank=True, verbose_name='Email')
    donante_phone = models.CharField(
        max_length=20, blank=True, verbose_name='Teléfono'
    )

    date = models.DateField()
    donation_type = models.CharField(max_length=20, choices=TIPO_CHOICES)
    status = models.CharField(
        max_length=15, choices=ESTADO_CHOICES, default='Pendiente'
    )

    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        verbose_name='Monto (€)'
    )

    payment_method = models.CharField(
        max_length=20, choices=METODO_PAGO_CHOICES,
        blank=True, verbose_name='Método de pago'
    )

    description = models.TextField(
        blank=True,
        help_text='Materiales donados, concepto del pago...'
    )

    def __str__(self):
        return f"{self.donation_type} — {self.donante} ({self.date})"

    class Meta:
        verbose_name = 'Donación'
        verbose_name_plural = 'Donaciones'
        ordering = ['-date']
