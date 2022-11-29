from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import check_password_hash
from pialara import db
from pialara.decorators import rol_required

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login')
def login():
    return render_template('auth/login.html')


@bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = db.get_user(email)
    # comprobamos si el usuario existe
    # cogemos la contraseña, la hasheamos y la comparamos con la contraseña hasheada
    if not user or not check_password_hash(user.password, password):
        flash('Por favor, comprueba tus datos y vuélvelo a intentar.')
        # si el usuario no existe, o está mal la contraseña, recargamos la página
        return redirect(url_for('auth.login'))

    # marcamos al usuario como autenticado en flask_login
    login_user(user, remember=remember)
    return redirect(url_for('auth.profile', nombre=current_user.nombre))


@bp.route('/profile')
def profile():
    return render_template('auth/profile.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada con éxito')
    return redirect(url_for('auth.login'))
