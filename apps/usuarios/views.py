from django.shortcuts import render, redirect
from .services.user_service import UserService
from django.contrib.auth import get_user_model


def usuarios(request):

    users = UserService.list_users()

    return render(request, 'usuarios/usuarios.html', {
        'users':users,
        "headertitle": "Gestión de Usuarios",
        "headersubtitle": "Listado de Usuarios",
        "btn_nuevo": "Nuevo Usuario",
        "form_url": 'usuarios_form',
        "btn_back": "Volver",
        "back_url": "home",
    })


def usuarios_delete(request, user_id):
     
    if request.method == "POST":

        UserService.delete_user(user_id)
    return redirect("usuarios")
 


def usuarios_form(request, user_id=None):

    # =========================
    # 📋 GET → mostrar formulario
    # =========================
    if request.method == "GET":

        user = None
        if user_id:
            user = UserService.get_user_by_id(user_id)

        return render(request, "usuarios/usuarios_form.html", {
            "user": user,
            "headertitle": "Gestión de Usuarios",
        "headersubtitle": "Registrar Nuevo Usuario",
        "btn_back": "Cancelar",
        "back_url": "usuarios"
        })

    # =========================
    # 💾 POST
    # =========================
    if request.method == "POST":

        # =========================
        # 🟡 CREATE / UPDATE
        # =========================
        
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        telefono = request.POST.get("telefono")
        descripcion = request.POST.get("descripcion")
        estado = request.POST.get("estado")
        role = request.POST.get("role")
         # mapear estado → is_active
        is_active = True if estado == "Activo" else False

        data = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "telefono": telefono,
        "descripcion": descripcion,
        "is_active": is_active,
        "roles": [role],  # 👈 lo convertimos a lista
    }

        if password:
            data["password"] = password


        if user_id:
            # ✏️ UPDATE
            UserService.update_user(user_id, **data)
        else:
            # 🆕 CREATE
            UserService.create_user(**data)

        return redirect("usuarios")



    #return render(request, 'usuarios/usuarios_form.html', {
     #   "headertitle": "Gestión de Usuarios",
      #  "headersubtitle": "Registrar Nuevo Usuario",
       # "btn_back": "Cancelar",
        #"back_url": "usuarios"
    #})


def roles(request):
    return render(request, 'usuarios/roles.html', {
        "headertitle": "Gestión de Usuarios",
        "headersubtitle": "Roles del Sistema",
        "btn_nuevo": "Nuevo Rol",
        "form_url": "roles_form",
        "btn_back": "Volver",
        "back_url": "home",
    })


def roles_form(request):
    return render(request, 'usuarios/roles_form.html', {
        "headertitle": "Gestión de Roles",
        "headersubtitle": "Registrar Nuevo Rol",
        "btn_back": "Cancelar",
        "back_url": "roles"
    })

def recuperar_contrasena(request):
    return render(request, 'usuarios/recuperar_contrasena.html', {
        "headertitle": "SafePaws",
        "headersubtitle": "Recuperación de Contraseña",
    })
