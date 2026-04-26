from django.shortcuts import render


def incidencias(request):
    return render(request, 'incidencias/incidencias.html', {
        "headertitle": "Gestión de Incidencias",
        "headersubtitle": "Listado de Incidencias",
        "btn_nuevo": "Nueva Incidencia",
        "form_url": 'incidencias_form',
        "btn_back": "Volver",
        "back_url": "home",
    })


def incidencias_form(request):
    return render(request, 'incidencias/incidencias_form.html', {
        "headertitle": "Gestión de incidencias",
        "headersubtitle": "Registro de Incidencias",
        "btn_back": "Cancelar",
        "back_url": "incidencias"
    })
