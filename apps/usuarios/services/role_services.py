from django.contrib.auth.models import Group, Permission
from django.db import transaction
from collections import defaultdict

class RoleService:

    LABELS = {
    "user": {"label": "Usuarios", "icon": "👤"},
    "group": {"label": "Roles", "icon": "🛡"},
    }

    # =========================
    # 🔵 READ (lista)
    # =========================
    @staticmethod
    def list_roles():
        roles = Group.objects.prefetch_related("permissions").all()

        for role in roles:
            role.permissions_list = role.permissions.all()

        return roles

    # =========================
    # 🔵 READ (uno)
    # =========================
    @staticmethod
    def get_role_by_id(role_id):
        role = Group.objects.prefetch_related("permissions").filter(id=role_id).first()

        if role:
            role.permissions_list = role.permissions.all()

        return role

    # =========================
    # 🟢 CREATE
    # =========================
    @staticmethod
    @transaction.atomic
    def create_role(name, permissions_ids=None):

        role = Group.objects.create(name=name)

        if permissions_ids is not None:
            permissions = Permission.objects.filter(id__in=permissions_ids)
            role.permissions.set(permissions)

        return role

    # =========================
    # 🟡 UPDATE
    # =========================
    @staticmethod
    @transaction.atomic
    def update_role(role_id, name=None, permissions_ids=None):

        role = Group.objects.filter(id=role_id).first()

        if not role:
            return None

        if name:
            role.name = name
            role.save(update_fields=["name"])

        if permissions_ids is not None:
            permissions = Permission.objects.filter(id__in=permissions_ids)
            role.permissions.set(permissions)

        return role

    # =========================
    # 🔴 DELETE
    # =========================
    @staticmethod
    @transaction.atomic
    def delete_role(role_id):

        role = Group.objects.filter(id=role_id).first()

        if not role:
            return False

        role.delete()
        return True

    # =========================
    # 🔵 LIST PERMISSIONS
    # =========================
    @staticmethod
    def list_permissions():
        return Permission.objects.select_related("content_type").all()
    

    
    @staticmethod
    def list_permissions_structured():
       

        permissions = Permission.objects.select_related("content_type").filter(
        content_type__app_label__in=["usuarios", "auth"],
        content_type__model__in=["user", "group"]
        )

        structured = {}

        for perm in permissions:
            app = perm.content_type.app_label
            model = perm.content_type.model
            codename = perm.codename

            key = f"{app}_{model}"

            # 🔥 SOLO LA PRIMERA VEZ CONFIGURAS LABEL E ICON
            if key not in structured:

                data = RoleService.LABELS.get(
                    model,
                    {"label": model.title(), "icon": ""}
                )

                structured[key] = {
                    "app": app,
                    "model": model,
                    "label": data["label"],
                    "icon": data["icon"],
                    "perms": {}
                }

            # 🔵 CRUD mapping
            if codename.startswith("add"):
                structured[key]["perms"]["create"] = perm
            elif codename.startswith("change"):
                structured[key]["perms"]["update"] = perm
            elif codename.startswith("delete"):
                structured[key]["perms"]["delete"] = perm
            elif codename.startswith("view"):
                structured[key]["perms"]["view"] = perm

        return dict(structured)