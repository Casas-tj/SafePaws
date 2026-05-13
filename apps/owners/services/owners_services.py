from apps.owners.models import Owner
from django.db import transaction


class OwnerService:

    # =========================
    # 🟢 CREATE
    # =========================
    @staticmethod
    @transaction.atomic
    def create_owner(name, last_name='', email='', phone='', address='', is_volunteer=False):
        owner = Owner.objects.create(
            name=name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            is_volunteer=is_volunteer,
        )
        return owner

    # =========================
    # 🔵 READ (uno)
    # =========================
    @staticmethod
    def get_owner_by_id(owner_id):
        owner = Owner.objects.filter(id=owner_id).first()
        if owner:
            owner.volunteer_label = "Si" if owner.is_volunteer else "No"
            owner.animals_list = owner.animals.filter(is_active=True)
            owner.adoptions_list = owner.adopciones.filter(is_active=True)
        return owner

    # =========================
    # 🔵 READ (lista)
    # =========================
    @staticmethod
    def list_owners():
        owners = Owner.objects.filter(is_active=True).order_by('name')
        for owner in owners:
            owner.volunteer_label = "Si" if owner.is_volunteer else "No"
        return owners

    # =========================
    # 🟡 UPDATE
    # =========================
    @staticmethod
    @transaction.atomic
    def update_owner(owner_id, **kwargs):
        owner = Owner.objects.filter(id=owner_id).first()

        if not owner:
            return None

        allowed = ['name', 'last_name', 'email',
                   'phone', 'address', 'is_volunteer']

        for key, value in kwargs.items():
            if key in allowed:
                setattr(owner, key, value)

        owner.save()
        return owner

    # =========================
    # 🔴 DELETE
    # =========================
    @staticmethod
    @transaction.atomic
    def delete_owner(owner_id):
        owner = Owner.objects.filter(id=owner_id).first()
        if not owner:
            return False
        owner.is_active = False
        owner.save(update_fields=["is_active"])
        return True
