from django.shortcuts import render


def voluntarios(request):
    return render(request, 'voluntarios/voluntarios.html', {
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
    return render(request, 'voluntarios/voluntarios_form.html', {
        "headertitle": "Gestión de Voluntarios",
        "headersubtitle": "Registrar Nuevo Voluntario",
        "btn_back": "Cancelar",
        "back_url": "voluntarios"
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })
