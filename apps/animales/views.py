from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.core.decorators import permisos_requeridos, requiere_permiso
from .services.animal_services import AnimalService
from apps.owners.services.owners_services import OwnerService


@permisos_requeridos('animales.view_animal')
def animales(request):

    animal = AnimalService.list_animals()

    return render(request, 'animales/animales.html', {
        'animales': animal,
        "headertitle": "Gestión de animales",
        "headersubtitle": "Listado de animales",
        "btn_nuevo": "Nuevo Animal",
        "form_url": 'animales_form',
        "nuevo_perm": "animales.add_animal",
        "btn_back": "Volver",
        "back_url": "home",
    })


@permisos_requeridos('animales.delete_animal')
def animales_delete(request, animal_id):
    if request.method == "POST":
        AnimalService.delete_animal(animal_id)
    return redirect("animales")


@login_required
def animales_form(request, animal_id=None):

    # =========================
    # 📋 GET → mostrar formulario
    # =========================
    if request.method == "GET":

        if animal_id:
            requiere_permiso(request, 'animales.change_animal')
        else:
            requiere_permiso(request, 'animales.add_animal')

        animal = None
        owner = None
        if animal_id:
            animal = AnimalService.get_animal_by_id(animal_id)
            if animal and animal.owner:
                owner = animal.owner

        owners = OwnerService.list_owners()
        return render(request, 'animales/animales_form.html', {
            "animal": animal,
            "owner": owner,
            "owners": owners,
            "headertitle": "Gestión de animales",
            "headersubtitle": "Registrar Nuevo Animal",
            "btn_back": "Cancelar",
            "back_url": "animales"
        })

    # =========================
    # 💾 POST
    # =========================
    if request.method == "POST":

        if animal_id:
            requiere_permiso(request, 'animales.change_animal')
        else:
            requiere_permiso(request, 'animales.add_animal')

        # =========================
        # 🟡 CREATE / UPDATE
        # =========================
        name = request.POST.get("name")
        species = request.POST.get("species")
        breed = request.POST.get("breed")
        age_years = request.POST.get("age_years")
        age_months = request.POST.get("age_months")
        sex = request.POST.get("sex")
        admission_date = request.POST.get("admission_date")
        vaccinated = request.POST.get("vaccinated")
        sterilized = request.POST.get("sterilized")
        status = request.POST.get("status")
        description = request.POST.get("description")
        owner_id = request.POST.get("owner_id")

        # mapear estado vacunado y esterilizado
        vaccinated = vaccinated == "Si"
        sterilized = sterilized == "Si"
        is_active = status == "Activo"

        data = {
            "name": name,
            "species": species,
            "breed": breed,
            "age_years": age_years,
            "age_months": age_months,
            "sex": sex,
            "admission_date": admission_date,
            "vaccinated": vaccinated,
            "sterilized": sterilized,
            "is_active": is_active,
            "description": description,
            "owner_id": owner_id,

        }

        if animal_id:
            # ✏️ UPDATE
            AnimalService.update_animal(animal_id, **data)
        else:
            # 🆕 CREATE
            AnimalService.create_animal(**data)

        return redirect("animales")


@permisos_requeridos('animales.view_animal')
def animales_details(request, animal_id):

    animal = AnimalService.get_animal_by_id(animal_id)
    if not animal:
        return redirect("animales")

    animal_nombre = animal.name if animal else "Animal"

    return render(request, "animales/animales_details.html", {
        "animal": animal,
        "headertitle": "Detalle del Animal",
        "headersubtitle": animal_nombre,
        "btn_back": "Volver",
        "back_url": "animales"
    })
