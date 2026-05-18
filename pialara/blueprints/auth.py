from typing import cast

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_limiter.util import get_remote_address
from flask_login import current_user as flask_current_user
from flask_login import login_required, login_user, logout_user
from flask_principal import (
    AnonymousIdentity,
    Identity,
    identity_changed,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,  # Haseo de la contraseña
)

from pialara import db, limiter
from pialara.models.User import User

current_user: User = cast(User, flask_current_user)

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.index"))
    return render_template("auth/login.html")


def limit_por_usuario():
    return request.form.get("email") or get_remote_address()


@bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute", key_func=limit_por_usuario)
@limiter.limit("20 per minute")
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for("users.index"))

    email = request.form.get("email")
    if not email:
        flash("El correo no puede estar vacío", "danger")
        return redirect(url_for("auth.login"))
    password = request.form.get("password")
    if not password:
        flash("La contraseña no puede estar vacía", "danger")
        return redirect(url_for("auth.login"))
    remember = True if request.form.get("remember") else False

    user = db.get_user(email)
    # comprobamos si el usuario existe
    # cogemos la contraseña, la hasheamos y la comparamos con la contraseña hasheada
    if not user or not check_password_hash(user.password, password):
        flash("Por favor, comprueba tus datos y vuélvelo a intentar", "danger")
        # si el usuario no existe, o está mal la contraseña, recargamos la página
        return redirect(url_for("auth.login"))

    # marcamos al usuario como autenticado en flask_login
    login_user(user, remember=remember)

    # actualizamos la identidad del usuario para flask_principal
    identity_changed.send(current_app, identity=Identity(user.get_id()))

    # le cambiamos la fecha de la última conexión
    db.update_ultima_conexion(email)

    # if user.rol == 'cliente':
    #     return redirect(url_for('audios.client_tag'))logged_rol = current_user.rol
    session["font_size"] = user.font_size

    return redirect(url_for("users.consent"))


@bp.route(
    "/email_rec_password",
)
def email_rec_password():
    return render_template("auth/email_rec_password.html")


@bp.route("/info_rec_password", methods=["GET", "POST"])
def info_rec_password():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            flash("El correo no puede estar vacío", "danger")
            return redirect(url_for("auth.email_rec_password"))
        nombre = request.form.get("nombre")
        if not nombre:
            flash("El nombre no puede estar vacío", "danger")
            return redirect(url_for("auth.email_rec_password"))

        user = db.get_user(email)

        if not user:
            flash("El correo introducido no está registrado", "danger")
            return redirect(url_for("auth.email_rec_password"))

        if user.nombre.lower().strip() != nombre.lower().strip():
            flash("El nombre no coincide con el correo introducido", "danger")
            return redirect(url_for("auth.email_rec_password"))

        # Guardamos temporalmente el email en la sesión para el siguiente paso
        session["email_reset"] = email

        flash("Datos verificados. Introduce tu nueva contraseña", "success")
        return redirect(url_for("auth.rec_password"))

    return render_template("auth/info_rec_password.html")


@bp.route("/rec_password", methods=["GET", "POST"])
def rec_password():
    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        if not new_password or not confirm_password:
            flash("Las contraseñas no pueden estar vacías", "danger")
            return redirect(url_for("auth.info_rec_password"))

        # Validacion para las contraseñas, tienen que coincidir
        if new_password != confirm_password:
            flash("Las contraseñas no coinciden", "danger")
            return redirect(url_for("auth.info_rec_password"))

        # mail de la sesión guardada
        email = session.get("email_reset")
        if not email:
            flash("Error: no se encontró la sesión de recuperación", "danger")
            return redirect(url_for("auth.email_rec_password"))

        user = db.get_user(email)
        if not user:
            flash("No se encontró el usuario", "danger")
            return redirect(url_for("auth.email_rec_password"))

        # hasheamos y actualizamos la nueva contraseña
        hashed_password = generate_password_hash(new_password)
        db.update_password(email, hashed_password)

        flash("Contraseña cambiada con éxito", "success")
        return redirect(url_for("auth.login"))

    # Si es GET, mostramos la página de cambio de contraseña
    return render_template("auth/info_rec_password.html")


@bp.route("/logout")
@login_required
def logout():
    session.pop("font_size", None)
    logout_user()
    identity_changed.send(current_app, identity=AnonymousIdentity())
    flash("Sesión cerrada con éxito", "success")
    return redirect(url_for("auth.login"))
