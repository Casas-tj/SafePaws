from apps.animales.models import Animal
from django.db import transaction


class AnimalService:

    # =========================
    # 🟢 CREATE
    # =========================
    @staticmethod
    @transaction.atomic
    def create_animal(name, species, breed=None, age_years=None, age_months=None,
                      sex=None, admission_date=None, vaccinated=False,
                      sterilized=False, is_active=True, description=None, owner_id=None):
        """
        Crea un animal en el refugio.
        is_active=True por defecto (animal en el refugio, activo).
        """
        animal = Animal.objects.create(
            name=name,
            species=species,
            breed=breed or '',
            age_years=age_years,
            age_months=age_months,
            sex=sex or '',
            admission_date=admission_date,
            vaccinated=vaccinated,
            sterilized=sterilized,
            is_active=is_active,
            description=description or '',
            owner_id=owner_id or None,
        )

        return animal

    # =========================
    # 🔵 READ (uno)
    # =========================
    @staticmethod
    def get_animal_by_id(animal_id):
        animal = Animal.objects.select_related(
            'owner').filter(id=animal_id).first()
        if animal:
            animal.status_label = "Activo" if animal.is_active else "Inactivo"
            animal.vaccinated_label = 'Si' if animal.vaccinated else "No"
            animal.sterilized_label = 'Si' if animal.sterilized else "No"
        return animal

    # =========================
    # 🔵 READ (lista) por orden activos
    # =========================
    @staticmethod
    def list_animals():
        animals = Animal.objects.filter(is_active=True).select_related(
            'owner').order_by('-created_at')
        for animal in animals:
            animal.status_label = "Activo" if animal.is_active else "Inactivo"
            animal.vaccinated_label = 'Si' if animal.vaccinated else "No"
            animal.sterilized_label = 'Si' if animal.sterilized else "No"
        return animals
    # =========================
    # 🔵 READ (lista) por orden inactivos
    # =========================

    @staticmethod
    def list_animals_inactive():
        animals = Animal.objects.filter(is_active=False).select_related(
            'owner').order_by('-created_at')
        for animal in animals:
            animal.status_label = "Activo" if animal.is_active else "Inactivo"
            animal.vaccinated_label = 'Si' if animal.vaccinated else "No"
            animal.sterilized_label = 'Si' if animal.sterilized else "No"
        return animals

    # =========================
    # 🟡 UPDATE
    # =========================
    @staticmethod
    @transaction.atomic
    def update_animal(animal_id, **kwargs):
        animal = Animal.objects.filter(id=animal_id).first()
        if not animal:
            return None
        allowed = ['name', 'species', 'breed', 'age_years', 'age_months', 'sex',
                   'admission_date', 'vaccinated', 'sterilized', 'is_active',
                   'description', 'owner_id']
        for attr, value in kwargs.items():
            if attr in allowed:
                setattr(animal, attr, value)
        animal.save()
        return animal

    # =========================
    # 🔴 DELETE
    # =========================
    @staticmethod
    @transaction.atomic
    def delete_animal(animal_id):
        animal = Animal.objects.filter(id=animal_id).first()
        if not animal:
            return False

        animal.is_active = False
        animal.save(update_fields=["is_active"])
        return True
