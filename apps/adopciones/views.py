from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.adopciones.services.adopciones_services import AdoptionService
from apps.animales.models import Animal
from apps.owners.models import Owner
from apps.core.decorators import permisos_requeridos


@permisos_requeridos("adopciones.view_adopcion")
def adopciones(request):

    adopciones_list = AdoptionService.list_adoptions()

    return render(request, 'adopciones/adopciones.html', {
        'adopciones': adopciones_list,
        'headertitle': 'Gestión de Adopciones',
        'headersubtitle': 'Listado de Adopciones',
        'btn_nuevo': 'Nueva Adopción',
        'form_url': 'adopciones_form',
        'btn_back': 'Volver',
        'back_url': 'home',
    })


@permisos_requeridos("adopciones.delete_adopcion")
def adopciones_delete(request, adoption_id):
    if request.method == "POST":
        AdoptionService.delete_adoption(adoption_id)
    return redirect("adopciones")


@permisos_requeridos("adopciones.add_adopcion", "adopciones.change_adopcion")
def adopciones_form(request, adoption_id=None):

    # =========================
    # 📋 GET → mostrar formulario
    # =========================
    if request.method == "GET":

        adoption = None
        if adoption_id:
            adoption = AdoptionService.get_adoption_by_id(adoption_id)

        animals = Animal.objects.filter(is_active=True).order_by('name')
        owners = Owner.objects.filter(is_active=True).order_by('name')

        return render(request, 'adopciones/adopciones_form.html', {
            'adoption': adoption,
            'animals': animals,
            'owners': owners,
            'headertitle': 'Gestión de Adopciones',
            'headersubtitle': 'Nueva Solicitud de Adopción',
            'btn_back': 'Cancelar',
            'back_url': 'adopciones',
        })

    # =========================
    # 💾 POST → guardar
    # =========================
    if request.method == "POST":

        animal_id = request.POST.get("animal_id")
        owner_id = request.POST.get("owner_id")
        adoption_date = request.POST.get("adoption_date") or None

        data = {
            "animal_id": animal_id,
            "owner_id": owner_id,
            "adoption_date": adoption_date,
        }

        if adoption_id:
            AdoptionService.update_adoption(adoption_id, **data)
        else:
            AdoptionService.create_adoption(**data)

        return redirect("adopciones")


@permisos_requeridos("adopciones.view_adopcion")
def adopciones_details(request, adoption_id):
    adopcion = AdoptionService.get_adoption_by_id(adoption_id)
    return render(request, 'adopciones/adopciones_details.html', {
        'adopcion': adopcion,
        'headertitle': 'Adopción',
        'headersubtitle': 'Detalles de la adopción',
        'btn_back': 'Volver',
        'back_url': 'adopciones',
    })
