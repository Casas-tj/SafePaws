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
    def create_user(username, password, email=None, first_name=None, last_name=None, telefono=None, descripcion=None, is_active=True, roles=None):
        user = User.objects.create_user(
            
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active
        )
        # Campos extra
        user.telefono = telefono
        user.descripcion = descripcion
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
        return User.objects.filter(id=user_id).first()

    # =========================
    # 🔵 READ (lista)
    # =========================
    @staticmethod
    def list_users():
        return User.objects.all().prefetch_related('groups')

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
            "telefono",
            "descripcion",
            "is_active",
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
        #DELETE
        #user.delete()
        #SOFTDELETE
        user.is_active = False
        user.save(update_fields=["is_active"])

        return True