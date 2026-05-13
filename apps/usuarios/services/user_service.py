from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction

User = get_user_model()


class UserService:

    # =========================
    # 🟢 CREATE
    # =========================
    @staticmethod
    @transaction.atomic
    def create_user(username, password, email=None, first_name=None, last_name=None, phone=None, description=None, is_active=True, is_volunteer=True, roles=None):
        user = User.objects.create_user(

            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            
        )
        # Campos extra
        user.is_active=is_active
        user.is_volunteer= is_volunteer
        user.phone = phone
        user.description = description
        user.save()

        if roles:
            groups = Group.objects.filter(name__in=roles)
            user.groups.set(groups)

        return user

    # =========================
    # 🔵 READ (uno)
    # =========================
    @staticmethod
    def get_user_by_id(user_id):
        user = User.objects.filter(id=user_id).first()

        if user:
            user.status_label = "Activo" if user.is_active else "Inactivo"
            user.volunteer_label = "Sí" if user.is_volunteer else "No"
            user.role_name = user.groups.first().name if user.groups.exists() else ""

        return user

    # =========================
    # 🔵 READ (lista) activos
    # =========================
    @staticmethod
    def list_users():
        users = User.objects.filter(is_active=True).prefetch_related('groups')
        for user in users:
            user.status_label = "Activo" if user.is_active else "Inactivo"
            user.volunteer_label = "Sí" if user.is_volunteer else "No"
            user.role_name = user.groups.first().name if user.groups.exists() else ""
        return users

    # =========================
    # 🔵 READ (lista) inactivos
    # =========================
    @staticmethod
    def list_users_inactive():
        users = User.objects.filter(is_active=False).prefetch_related('groups')
        for user in users:
            user.status_label = "Inactivo"
            user.volunteer_label = "Sí" if user.is_volunteer else "No"
            user.role_name = user.groups.first().name if user.groups.exists() else ""
        return users
    # =========================
    # 🟡 UPDATE
    # =========================

    @staticmethod
    @transaction.atomic
    def update_user(user_id, **kwargs):

        user = User.objects.filter(id=user_id).first()

        if not user:
            return None

        password = kwargs.pop('password', None)
        roles = kwargs.pop('roles', None)

        allowed_fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "description",
            "is_active",
            "is_volunteer"
        ]

        for attr, value in kwargs.items():
            if attr in allowed_fields:
                setattr(user, attr, value)

        # password (especial)
        if password:
            user.set_password(password)

        # roles (especial)
        if roles is not None:
            groups = Group.objects.filter(name__in=roles)
            user.groups.set(groups)

        user.save()
        return user

    # =========================
    # 🔴 DELETE
    # =========================
    @staticmethod
    @transaction.atomic
    def delete_user(user_id):
        user = User.objects.filter(id=user_id).first()

        if not user:
            return False

        # DELETE
        # user.delete()
        # SOFTDELETE
        user.is_active = False
        user.save(update_fields=["is_active"])

        return True
