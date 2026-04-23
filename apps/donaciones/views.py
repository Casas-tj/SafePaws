from django.shortcuts import render


def donaciones(request):
    return render(request, 'donaciones/donaciones.html', {
        "headertitle": "Gestión de Donaciones",
        "headersubtitle": "Listado de Donaciones",
        "btn_nuevo": "Nueva Donación",
        "form_url": 'donaciones_form',
        "btn_back": "Volver",
        "back_url": "home",
    })


def donaciones_form(request):
    return render(request, 'donaciones/donaciones_form.html', {
        "headertitle": "Gestión de donaciones",
        "headersubtitle": "Registrar Nueva Donación",
        "btn_back": "Cancelar",
        "back_url": "donaciones"
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })
