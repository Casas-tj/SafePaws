from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import PasswordResetTicket
from .services.user_service import UserService
from .services.role_services import RoleService
from apps.core.decorators import permisos_requeridos


@permisos_requeridos("usuarios.view_user")
def usuarios(request):

    users = UserService.list_users()

    return render(request, 'usuarios/usuarios.html', {
        'users': users,
        "headertitle": "Gestión de Usuarios",
        "headersubtitle": "Listado de Usuarios",
        "btn_nuevo": "Nuevo Usuario",
        "form_url": 'usuarios_form',
        "btn_back": "Volver",
        "back_url": "home",
    })


@permisos_requeridos("usuarios.delete_user")
def usuarios_delete(request, user_id):

    if request.method == "POST":

        UserService.delete_user(user_id)
    return redirect("usuarios")


@permisos_requeridos("usuarios.add_user", "usuarios.change_user")
def usuarios_form(request, user_id=None):

    # =========================
    # 📋 GET → mostrar formulario
    # =========================
    if request.method == "GET":

        user = None
        if user_id:
            user = UserService.get_user_by_id(user_id)

        roles = RoleService.list_roles()

        return render(request, "usuarios/usuarios_form.html", {
            "user": user,
            "roles": roles,
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
        phone = request.POST.get("phone")
        description = request.POST.get("description")
        status = request.POST.get("status")
        volunteer = request.POST.get("volunteer")
        role = request.POST.get("role")
        # mapear estado → is_active
        is_active = True if status == "Activo" else False
        is_volunteer = True if volunteer == "Si" else False

        data = {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "description": description,
            "is_active": is_active,
            "is_volunteer": is_volunteer,
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


@permisos_requeridos("auth.view_group")
def roles(request):

    roles = RoleService.list_roles()

    return render(request, 'usuarios/roles.html', {
        "roles": roles,
        "headertitle": "Gestión de Usuarios",
        "headersubtitle": "Roles del Sistema",
        "btn_nuevo": "Nuevo Rol",
        "form_url": "roles_form",
        "btn_back": "Volver",
        "back_url": "home",
    })


@permisos_requeridos("auth.delete_group")
def roles_delete(request, role_id):
    if request.method == "POST":
        RoleService.delete_role(role_id)

    return redirect("roles")


@permisos_requeridos("auth.add_group", "auth.change_group")
def roles_form(request, role_id=None):

    # =========================
    # 📋 GET → mostrar formulario
    # =========================
    if request.method == "GET":

        role = None
        if role_id:
            role = RoleService.get_role_by_id(role_id)

        permissions = RoleService.list_permissions_structured()

        return render(request, "usuarios/roles_form.html", {
            "role": role,
            "permissions": permissions,
            "headertitle": "Gestión de Roles",
            "headersubtitle": "Crear / Editar Rol",
            "btn_back": "Cancelar",
            "back_url": "roles"
        })

    # =========================
    # 💾 POST → guardar
    # =========================
    if request.method == "POST":

        name = request.POST.get("name")
        permissions = request.POST.getlist("permissions")

        if role_id:
            # ✏️ UPDATE
            RoleService.update_role(role_id, name, permissions)
        else:
            # 🆕 CREATE
            RoleService.create_role(name, permissions)

        return redirect("roles")

    return render(request, 'usuarios/roles_form.html', {
        "headertitle": "Gestión de Roles",
        "headersubtitle": "Registrar Nuevo Rol",
        "btn_back": "Cancelar",
        "back_url": "roles"
    })


def recuperar_contrasena(request):
    ticket_creado = False
    ticket_id = None

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        reason = request.POST.get("recovery_reason", "").strip()

        if email and reason:
            ticket = PasswordResetTicket.objects.create(email=email, reason=reason)
            ticket_creado = True
            ticket_id = ticket.id

    return render(request, 'usuarios/recuperar_contrasena.html', {
        "headertitle": "SafePaws",
        "headersubtitle": "Recuperación de Contraseña",
        "ticket_creado": ticket_creado,
        "ticket_id": ticket_id,
    })


@permisos_requeridos("usuarios.view_passwordresetticket")
def tickets_list(request):
    tickets = PasswordResetTicket.objects.all()
    return render(request, 'usuarios/tickets_list.html', {
        'tickets': tickets,
        "headertitle": "Tickets de recuperación",
        "headersubtitle": "Solicitudes de restablecimiento de contraseña",
        "btn_back": "Volver",
        "back_url": "home",
    })


@permisos_requeridos("usuarios.change_passwordresetticket")
def tickets_resolve(request, ticket_id):
    ticket = PasswordResetTicket.objects.filter(id=ticket_id, status='Pendiente').first()
    if not ticket:
        return redirect('tickets_list')

    resolved = False
    error = None

    if request.method == "POST":
        new_password = request.POST.get("new_password", "").strip()
        if len(new_password) < 4:
            error = "La contraseña debe tener al menos 4 caracteres"
        else:
            user = get_user_model().objects.filter(email=ticket.email).first()
            if user:
                user.set_password(new_password)
                user.save()

            ticket.status = 'Resuelto'
            ticket.resolved_at = timezone.now()
            ticket.resolved_by = request.user
            ticket.save()
            resolved = True

    return render(request, 'usuarios/tickets_resolve.html', {
        'ticket': ticket,
        'resolved': resolved,
        'error': error,
        "headertitle": "Resolver ticket",
        "headersubtitle": f"Ticket #{ticket.id} — {ticket.email}",
        "btn_back": "Volver",
        "back_url": "tickets_list",
    })
