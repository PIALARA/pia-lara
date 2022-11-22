from flask import Blueprint, render_template
from flask_login import login_required, current_user
from pialara.db import db
from pialara.models.Usuario import Usuario

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/')
@login_required
def index():
    u = Usuario()

    logged_rol = current_user.rol
    if logged_rol == "Administrador":
        users = db.users.find()
    else:
        raise Exception("Operación no permitida para el rol", logged_rol)


    return render_template('users/index.html', users=u.find())
