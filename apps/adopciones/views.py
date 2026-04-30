from django.shortcuts import render, redirect
from apps.adopciones.services.adopciones_services import AdoptionService
from .models import Adopcion


def adopciones(request):

    adopciones = AdoptionService.list_adoptions()

    return render(request, 'adopciones/adopciones.html', {
        "adopciones": adopciones,
        "headertitle": "Gestión de Adopciones",
        "headersubtitle": "Listado de Adopciones",
        "btn_nuevo": "Nueva Adopción",
        "form_url": 'adopciones_form',
        "btn_back": "Volver",
        "back_url": "home",
    })


def adopciones_delete(request, adoption_id):
    if request.method == "POST":
        AdoptionService.delete_adoption(adoption_id)
    return redirect("adopciones")


def adopciones_form(request, adoption_id=None):

    # =========================
    # 📋 GET → mostrar formulario
    # =========================
    if request.method == "GET":

        adoption = None
        if adoption_id:
            adoption = AdoptionService.get_adoption_by_id(adoption_id)

        return render(request, 'adopciones/adopciones_form.html', {
            "adoption": adoption,
            "headertitle": "Gestión de Adopciones",
            "headersubtitle": "Nueva Solicitud de Adopción",
            "btn_back": "Cancelar",
            "back_url": "adopciones"
        })

    # =========================
    # 💾 POST
    # =========================
    if request.method == "POST":

        # =========================
        # 🟡 CREATE / UPDATE
        # =========================

        animal_id = request.POST.get("animal_id")
        adoption_id = request.POST.get("adoption_id")
        adopter_name = request.POST.get("adopter_name")
        phone = request.POST.get("phone")
        adoptant_email = request.POST.get("adoptant_email")
        adoptant_address = request.POST.get("adoptant_address")
        observations = request.POST.get("observations")
        adoption_status = request.POST.get("adoption_status")
        adoption_date = request.POST.get("adoption_date")

        data = {
            "animal_id": animal_id,
            "adoption_id": adoption_id,
            "adoptant_name": adoptant_name,
            "adoptant_phone": adoptant_phone,
            "adoptant_email": adoptant_email,
            "adoptant_address": adoptant_address,
            "adoption_date": adoption_date,
            "adoption_status": adoption_status,
            "observations": observations,
        }

        if adoption_id:
            # ✏️ UPDATE
            AdoptionService.update_adoption(adoption_id, **data)
        else:
            # 🆕 CREATE
            AdoptionService.create_adoption(**data)
        return redirect("adopciones")
