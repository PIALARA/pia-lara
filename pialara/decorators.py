from functools import wraps
import flask_login
from flask import render_template

def rol_required(rol):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if hasattr(flask_login.current_user, 'rol') and (flask_login.current_user.rol == rol):
                return fn(*args, **kwargs)

            return render_template('auth/login.html')
 
        return decorator
 
    return wrapper