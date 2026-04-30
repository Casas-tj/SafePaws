from apps.adopciones.models import Adopcion
from django.db import transaction


class AdoptionService:

    # =========================
    # 🟢 CREATE
    # =========================
    @staticmethod
    @transaction.atomic
    def create_adoption(animal_id, adoptant_name, adoptant_phone, adoptant_email, adoptant_address=None, status='En Proceso', fecha_solicitud=None, fecha_adopcion=None, observaciones=None):
        adoption = Adopcion.objects.create(
            animal_id=animal_id,
            adoptante_nombre=adoptant_name,
            adoptante_telefono=adoptant_phone,
            adoptante_email=adoptant_email,
            adoptante_direccion=adoptant_address,
            status=status,
            fecha_solicitud=fecha_solicitud,
            fecha_adopcion=fecha_adopcion,
            observaciones=observaciones
        )

        return adoption

    # =========================
    # 🔵 READ (uno)
    # =========================

    @staticmethod
    def get_adoption_by_id(adoption_id):
        return Adopcion.objects.filter(id=adoption_id).first()

    # =========================
    # 🔵 READ (lista) por orden
    # =========================
    @staticmethod
    def list_adoptions():
        return Adopcion.objects.all().order_by("-created_at")

    # =========================
    # 🟡 UPDATE
    # =========================
    @staticmethod
    @transaction.atomic
    def update_adoption(adoption_id, **kwargs):

        adoption = Adopcion.objects.filter(id=adoption_id).first()

        if not adoption:
            return ValueError("Adoption not found")

        allowed_fields = [
            "animal_id",
            "adoptante_nombre",
            "adoptante_telefono",
            "adoptante_email",
            "adoptante_direccion",
            "status",
            "admission_date",
        ]

        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(adoption, key, value)
        adoption.save()
        return adoption

    # =========================
    # 🔴 DELETE
    # =========================

    @staticmethod
    @transaction.atomic
    def delete_adoption(adoption_id):
        adoption = Adopcion.objects.filter(id=adoption_id).first()

        if not adoption:
            raise ValueError("Adoption not found")

        adoption.delete()
        return True
    
    
