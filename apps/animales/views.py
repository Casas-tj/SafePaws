from django.shortcuts import render, redirect
from .services.animal_services import AnimalService
from .models import Animal


def animales(request):

    animales = AnimalService.list_animals()

    return render(request, 'animales/animales.html', {
        'animales': animales,
        'headertitle': 'Gestión de animales',
        'headersubtitle': 'Listado de animales',
        'btn_nuevo': 'Nuevo Animal',
        'form_url': 'animales_form',
        'btn_back': 'Volver',
        'back_url': 'home',
    })


def animales_delete(request, animal_id):
    if request.method == "POST":
        AnimalService.delete_animal(animal_id)
    return redirect("animales")


def animales_form(request, animal_id=None):

    # =========================
    # 📋 GET → mostrar formulario
    # =========================
    if request.method == "GET":

        animal = None
        if animal_id:
            animal = AnimalService.get_animal_by_id(animal_id)

        return render(request, 'animales/animales_form.html', {
            "animal": animal,
            "headertitle": "Gestión de animales",
            "headersubtitle": "Registrar Nuevo Animal",
            "btn_back": "Cancelar",
            "back_url": "animales"
        })

    # =========================
    # 💾 POST
    # =========================
    if request.method == "POST":

        # =========================
        # 🟡 CREATE / UPDATE
        # =========================

        name = request.POST.get("name")
        species = request.POST.get("species")
        breed = request.POST.get("breed")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        status = request.POST.get("status")
        admission_date = request.POST.get("admission_date")
        vaccinated = request.POST.get("vaccinated")
        spayed = request.POST.get("spayed")
        description = request.POST.get("description")

        data = {
            "name": name,
            "species": species,
            "breed": breed,
            "age": age,
            "gender": gender,
            "status": status,
            "admission_date": admission_date,
            "vaccinated": vaccinated,
            "spayed": spayed,
            "description": description
        }

        if animal_id:
            # ✏️ UPDATE
            AnimalService.update_animal(animal_id, **data)
        else:
            # 🆕 CREATE
            AnimalService.create_animal(**data)

        return redirect("animales")
