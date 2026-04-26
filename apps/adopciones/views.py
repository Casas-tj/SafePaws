from django.shortcuts import render


def adopciones(request):
    return render(request, 'adopciones/adopciones.html', {
        "headertitle": "Gestión de Adopciones",
        "headersubtitle": "Listado de Adopciones",
        "btn_nuevo": "Nueva Adopción",
        "form_url": 'adopciones_form',
        "btn_back": "Volver",
        "back_url": "home",
    })


def adopciones_form(request):
    return render(request, 'adopciones/adopciones_form.html', {
        "headertitle": "Gestión de Adopciones",
        "headersubtitle": "Nueva Solicitud de Adopción",
        "btn_back": "Cancelar",
        "back_url": "adopciones"
    })
