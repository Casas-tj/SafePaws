from django.shortcuts import render


def voluntarios(request):
    return render(request, 'voluntarios.html', {
        "headertitle": "Gestión de Voluntarios",
        "headersubtitle": "Listado de Voluntarios",
        "btn_nuevo": "Nuevo Voluntario",
        "form_url": "voluntarios_form",
        "btn_back": "Volver",
        "back_url": "home",
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })


def voluntarios_form(request):
    return render(request, 'voluntarios_form.html', {
        "headertitle": "Gestión de Voluntarios",
        "headersubtitle": "Registrar Nuevo Voluntario",
        "btn_back": "Cancelar",
        "back_url": "voluntarios"
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })


def funciones(request):
    return render(request, 'funciones.html', {
        "headertitle": "Gestión de Voluntarios",
        "headersubtitle": "Tareas que hace cada voluntario",
        "btn_back": "Volver",
        "back_url": "home",
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })
