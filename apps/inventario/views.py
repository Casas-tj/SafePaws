from django.shortcuts import render


def suministros(request):
    return render(request, 'inventario/suministros.html', {
        "headertitle": "Gestión de Suministros",
        "headersubtitle": "Lista de Suministros",
        "btn_back": "Volver",
        "back_url": "home",
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })


def inventario(request):
    return render(request, 'inventario/inventario.html', {
        "headertitle": "Gestión de Inventario",
        "headersubtitle": "Listado de Inventario",
        "btn_nuevo": "Añadir Nuevo Producto",
        "form_url": 'inventario',
        "btn_back": "Cancelar",
        "back_url": "suministros",
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })


def stock(request):
    return render(request, 'inventario/stock.html', {
        "headertitle": "Gestión de Stock",
        "headersubtitle": "Lista de Stock",
        "btn_nuevo": "Registrar Nuevo Producto",
        "form_url": 'stock',
        "btn_back": "Cancelar",
        "back_url": "suministros",
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })
