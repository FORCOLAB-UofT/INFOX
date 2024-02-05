from functools import wraps

from flask import abort
from flask_login import current_user

from .models import Permission


def permission_required(permission):
    """ permission_required decorator
        Args:
            permission: the permission
        Returns:
            decorator
    """
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return inner
    return decorator


def admin_required(f):
    """ admin verify
        Args
            f: view approach
        Returns:
            decorator
    """
    return permission_required(Permission.ADMINISTER)(f)
