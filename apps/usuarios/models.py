from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.models import TimeStampedModel

class User(TimeStampedModel,AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_volunteer = models.BooleanField(default=False)

    def __str__(self):
        return self.username
