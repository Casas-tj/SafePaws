from apps.animales.models import Animal
from django.db import transaction


class AnimalService:

    # =========================
    # 🟢 CREATE
    # =========================
    @staticmethod
    @transaction.atomic
    def create_animal(name, species, breed=None, age=None, gender=None, status='En Adopcion', admission_date=None, vaccinated=None, spayed=False, description=None):
        animal = Animal.objects.create(
            nombre=name,
            especie=species,
            raza=breed,
            edad=age,
            sexo=gender,
            estado=status,
            fecha_adopcion=admission_date,
            vacunado=vaccinated,
            esterilizado=spayed,
            descripcion=description
        )

        return animal

    # =========================
    # 🔵 READ (uno)
    # =========================
    @staticmethod
    def get_animal_by_id(animal_id):
        return Animal.objects.filter(id=animal_id).first()

    # =========================
    # 🔵 READ (lista) por orden
    # =========================
    @staticmethod
    def list_animals():
        return Animal.objects.all().order_by("-created_at")

    # =========================
    # 🔵 READ (lista) por estado
    # =========================
    @staticmethod
    def list_animals_by_status(status):
        return Animal.objects.filter(status=status).order_by("-created_at")

    # =========================
    # 🟡 UPDATE
    # =========================
    @staticmethod
    @transaction.atomic
    def update_animal(animal_id, **kwargs):

        animal = Animal.objects.filter(id=animal_id).first()

        if not animal:
            return None

        animal.name = kwargs.pop("name", animal.name)
        animal.species = kwargs.pop("species", animal.species)
        animal.breed = kwargs.pop("breed", animal.breed)
        animal.age = kwargs.pop("age", animal.age)
        animal.gender = kwargs.pop("gender", animal.gender)
        animal.status = kwargs.pop("status", animal.status)
        animal.admission_date = kwargs.pop(
            "admission_date", animal.admission_date)

        allowed_fields = [
            "name",
            "species",
            "breed",
            "gender",
            "status",
            "admission_date",
        ]

        for attr, value in kwargs.items():
            if attr in allowed_fields:
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

        animal.delete()
        return True
