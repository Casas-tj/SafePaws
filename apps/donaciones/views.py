from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .services.donacion_services import DonationService


@login_required
def donaciones(request):

    donations = DonationService.list_donaciones()

    return render(request, 'donaciones/donaciones.html', {
        "donations": donations,
        "headertitle": "Gestión de Donaciones",
        "headersubtitle": "Listado de Donaciones",
        "btn_nuevo": "Nueva Donación",
        "form_url": 'donaciones_form',
        "btn_back": "Volver",
        "back_url": "home",
    })


@login_required
def donaciones_delete(request, donation_id):
    if request.method == "POST":
        DonationService.delete_donation(donation_id)
    return redirect("donaciones")


@login_required
def donaciones_form(request, donation_id=None):

    # =========================
    # 📋 GET → mostrar formulario
    # =========================
    if request.method == "GET":
        donation = None
        if donation_id:
            donation = DonationService.get_donation_by_id(donation_id)

        return render(request, 'donaciones/donaciones_form.html', {
            "donation": donation,
            "headertitle": "Gestión de donaciones",
            "headersubtitle": "Registrar Nueva Donación",
            "btn_back": "Cancelar",
            "back_url": "donaciones"
        })

    # =========================
    # 💾 POST
    # =========================
    if request.method == "POST":

        # =========================
        # 🟡 CREATE / UPDATE
        # =========================
        donante = request.POST.get("donante")
        donante_email = request.POST.get("donante_email")
        donante_phone = request.POST.get("donante_phone")
        date = request.POST.get("date")
        donation_type = request.POST.get("donation_type")
        status = request.POST.get("status")
        description = request.POST.get("description")
        amount = request.POST.get("amount") or None
        payment_method = request.POST.get("payment_method")

        data = {
            "donante": donante,
            "donante_email": donante_email,
            "donante_phone": donante_phone,
            "date": date,
            "donation_type": donation_type,
            "status": status,
            "description": description,
            "amount": amount,
            "payment_method": payment_method
        }

        if donation_id:
            DonationService.update_donation(donation_id, **data)
        else:
            DonationService.create_donation(**data)
        return redirect("donaciones")


@login_required
def donaciones_details(request, donation_id):
    donation = DonationService.get_donation_by_id(donation_id)
    return render(request, 'donaciones/donaciones_details.html', {
        'donation': donation,
        'headertitle': 'Donación',
        'headersubtitle': 'Detalles de la donación',
        'btn_back': 'Volver',
        'back_url': 'donaciones',
    })
