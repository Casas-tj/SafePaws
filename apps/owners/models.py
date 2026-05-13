from django.db import models
from apps.core.models import TimeStampedModel


class Owner(TimeStampedModel):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_volunteer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.last_name}".strip()

    class Meta:
        verbose_name = 'Owner'
        verbose_name_plural = 'Owners'
        ordering = ['name']
