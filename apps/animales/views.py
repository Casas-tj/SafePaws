from django.shortcuts import render


def animales(request):
    return render(request, 'animales/animales.html', {
        "headertitle": "Gestión de animales",
        "headersubtitle": "Listado de animales",
        "btn_nuevo": "Nuevo Animal",
        "form_url": 'animales_form',
        "btn_back": "Volver",
        "back_url": "home",
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })


def animales_form(request):
    return render(request, 'animales/animales_form.html', {
        "headertitle": "Gestión de animales",
        "headersubtitle": "Registrar Nuevo Animal",
        "btn_back": "Cancelar",
        "back_url": "animales"
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })
