from django.shortcuts import render


def recuperar_contrasena(request):
    return render(request, 'usuarios/recuperar_contrasena.html', {
        "headertitle": "SafePaws",
        "headersubtitle": "Recuperación de Contraseña",
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })


def usuarios(request):
    return render(request, 'usuarios/usuarios.html', {
        "headertitle": "Gestión de Usuarios",
        "headersubtitle": "Listado de Usuarios",
        "btn_nuevo": "Nuevo Usuario",
        "form_url": 'usuarios_form',
        "btn_back": "Volver",
        "back_url": "home",
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })


def usuarios_form(request):
    return render(request, 'usuarios/usuarios_form.html', {
        "headertitle": "Gestión de Usuarios",
        "headersubtitle": "Registrar Nuevo Usuario",
        "btn_back": "Cancelar",
        "back_url": "usuarios"
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })


def roles(request):
    return render(request, 'usuarios/roles.html', {
        "headertitle": "Gestión de Usuarios",
        "headersubtitle": "Roles del Sistema",
        "btn_nuevo": "Nuevo Rol",
        "form_url": "roles",
        "btn_back": "Volver",
        "back_url": "home",
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })
