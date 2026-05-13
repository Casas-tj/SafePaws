from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import random

User = get_user_model()


class Command(BaseCommand):  # 👈 ESTO ES OBLIGATORIO
    help = "Crea usuarios de prueba"

    def handle(self, *args, **kwargs):

        roles = list(Group.objects.all())

        if not roles:
            self.stdout.write(self.style.ERROR("No hay roles creados"))
            return

        for i in range(12, 30):
            username = f"user{i}"

            if User.objects.filter(username=username).exists():
                continue

            user = User.objects.create_user(
                username=username,
                password="123456",
                email=f"user{i}@test.com",
                first_name=f"Nombre{i}",
                last_name=f"Apellido{i}",
                is_active=True
            )

            # 🔹 campos extra del modelo
            user.telefono = f"+56900000{i}"
            user.descripcion = f"Usuario de prueba {i}"
            user.save()

            role = random.choice(roles)
            user.groups.add(role)

            self.stdout.write(f"{username} → {role.name}")

        self.stdout.write(self.style.SUCCESS("Seed completado"))