from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Crea los roles iniciales del sistema"

    def handle(self, *args, **kwargs):
        roles = [
            "Administrador",
            "Veterinario",
            "Cuidador",
            "Recepcionista",
            "Voluntario"
        ]

        for role in roles:
            Group.objects.get_or_create(name=role)

        self.stdout.write(self.style.SUCCESS("Roles creados correctamente"))