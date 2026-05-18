from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps


def permisos_requeridos(*perms):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            for perm in perms:
                if not request.user.has_perm(perm):
                    raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def requiere_permiso(request, perm):
    if request.user.is_superuser:
        return
    if not request.user.has_perm(perm):
        raise PermissionDenied
