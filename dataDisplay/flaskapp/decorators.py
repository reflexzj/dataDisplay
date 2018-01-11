# -*- coding: utf-8 -*-
"""permission required"""

from functools import wraps
from flask import abort

from flask_login import current_user


def permission_required(permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.check_permission(permissions):
                abort(403)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def delete_required(func):
    return permission_required(8)(func)


def update_required(func):
    return permission_required(4)(func)


def input_required(func):
    return permission_required(2)(func)

