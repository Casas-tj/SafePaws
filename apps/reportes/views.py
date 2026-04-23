from django.shortcuts import render


def reportes(request):
    return render(request, 'reportes/reportes.html', {
        "headertitle": "Gestión de Reportes",
        "headersubtitle": "Listado de Reportes",
        "btn_back": "Volver",
        "back_url": "home",
    })


def reporte_inventario(request):
    return render(request, 'reportes/reporte_inventario.html', {
        "headertitle": "Gestión de Inventario",
        "headersubtitle": "Reportes de Inventario",
        "btn_nuevo": "Nuevo Reporte de Inventario",
        "form_url": 'reporte_inventario',
        "btn_back": "Cancelar",
        "back_url": "reportes",
        "show_report_buttons": True
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })


def reporte_adopciones(request):
    return render(request, 'reportes/reporte_adopciones.html', {
        "headertitle": "Gestión de Inventario",
        "headersubtitle": "Reportes de Adopciones",
        "btn_nuevo": "Nuevo Reporte de Adopciones",
        "form_url": 'reporte_adopciones',
        "btn_back": "Cancelar",
        "back_url": "reportes",
        "show_report_buttons": True
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })
