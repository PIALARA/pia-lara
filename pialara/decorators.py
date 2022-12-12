from functools import wraps
import flask_login
from flask import render_template

def rol_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            authorized = False
            for rol in roles:
                if hasattr(flask_login.current_user, 'rol') and (flask_login.current_user.rol == rol):
                    authorized = True
                
            if authorized:
                return fn(*args, **kwargs)

            return render_template('auth/login.html')
 
        return decorator
 
    return wrapper