from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.models import TimeStampedModel


class User(TimeStampedModel, AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_volunteer = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class PasswordResetTicket(models.Model):
    email = models.EmailField(verbose_name='Correo electrónico')
    reason = models.TextField(verbose_name='Motivo de la solicitud')
    status = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('Resuelto', 'Resuelto')],
        default='Pendiente',
        verbose_name='Estado',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name='Resuelto el')
    resolved_by = models.ForeignKey(
        'usuarios.User', null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Resuelto por',
    )

    def __str__(self):
        return f'Ticket {self.id} — {self.email} ({self.status})'

    class Meta:
        verbose_name = 'Ticket de recuperación'
        verbose_name_plural = 'Tickets de recuperación'
        ordering = ['-created_at']
