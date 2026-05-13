from apps.adopciones.models import Adopcion
from django.db import transaction


class AdoptionService:

    # =========================
    # 🟢 CREATE
    # =========================
    @staticmethod
    @transaction.atomic
    def create_adoption(animal_id, owner_id, adoption_date=None, is_active=True):
        adoption = Adopcion.objects.create(
            animal_id=animal_id,
            owner_id=owner_id,
            adoption_date=adoption_date,
        )

        adoption.is_active = is_active
        adoption.save()
        return adoption

    # =========================
    # 🔵 READ (uno)
    # =========================
    @staticmethod
    def get_adoption_by_id(adoption_id):
        return Adopcion.objects.select_related('animal', 'owner').filter(id=adoption_id).first()

    # ===============================
    # 🔵 READ (lista) solo activas
    # ===============================
    @staticmethod
    def list_adoptions():
        return Adopcion.objects.select_related('animal', 'owner').filter(is_active=True).order_by('-created_at')

    # =========================
    # 🟡 UPDATE
    # =========================
    @staticmethod
    @transaction.atomic
    def update_adoption(adoption_id, **kwargs):
        adoption = Adopcion.objects.filter(id=adoption_id).first()
        if not adoption:
            return None
        allowed = ['animal_id', 'owner_id', 'adoption_date']
        for key, value in kwargs.items():
            if key in allowed:
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
            return None
        adoption.is_active = False
        adoption.save(update_fields=['is_active'])
        return True
