from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.core.decorators import permisos_requeridos, requiere_permiso
from apps.owners.services.owners_services import OwnerService


@permisos_requeridos('owners.view_owner')
def owners(request):

    owners = OwnerService.list_owners()

    return render(request, 'owners/owners.html', {
        'owners': owners,
        'headertitle': 'Cuidadores',
        'headersubtitle': 'Listado de propietarios y adoptantes',
        "btn_nuevo": "Nuevo Propietario",
        "form_url": 'owners_form',
        "nuevo_perm": "owners.add_owner",
        'btn_back': 'Volver',
        'back_url': 'home',
    })


@login_required
def owners_form_edit(request, owner_id=None):

    # =========================
    # 📋 GET → mostrar formulario
    # =========================
    if request.method == "GET":

        if owner_id:
            requiere_permiso(request, 'owners.change_owner')
        else:
            requiere_permiso(request, 'owners.add_owner')

        owner = None
        if owner_id:
            owner = OwnerService.get_owner_by_id(owner_id)

        return render(request, 'owners/owners_form.html', {
            'owner': owner,
            'headertitle': 'Cuidadores',
            'headersubtitle': 'Registrar nuevo propietario',
            'btn_back': 'Cancelar',
            'back_url': 'owners',
        })

    # =========================
    # 💾 POST → guardar
    # =========================
    if request.method == "POST":

        if owner_id:
            requiere_permiso(request, 'owners.change_owner')
        else:
            requiere_permiso(request, 'owners.add_owner')

        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        volunteer = request.POST.get("volunteer")
        is_volunteer = volunteer == "Si"

        data = {
            'name': name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'address': address,
            'is_volunteer': is_volunteer,
        }

        if owner_id:
            # ✏️ UPDATE
            OwnerService.update_owner(owner_id, **data)
        else:
            # 🆕 CREATE
            OwnerService.create_owner(**data)

        return redirect('owners')


@permisos_requeridos('owners.delete_owner')
def owners_delete(request, owner_id):
    if request.method == "POST":
        OwnerService.delete_owner(owner_id)
    return redirect('owners')


@permisos_requeridos('owners.view_owner')
def owners_details(request, owner_id):
    owner = OwnerService.get_owner_by_id(owner_id)
    return render(request, 'owners/owners_details.html', {
        'owner': owner,
        'headertitle': 'Propietario',
        'headersubtitle': 'Detalles del propietario',
        'btn_back': 'Volver',
        'back_url': 'owners',
    })
