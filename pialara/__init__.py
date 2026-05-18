import configparser
import os
from typing import cast

from flask import Flask, jsonify, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_login import current_user as flask_current_user
from flask_principal import Principal, RoleNeed, UserNeed, identity_loaded
from werkzeug.middleware.proxy_fix import ProxyFix

from pialara import db
from pialara.models.User import User

current_user = cast(User, flask_current_user)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",  # Para producción: "redis://localhost:6379" (necesario redis)
)


def create_app():
    # create and configure the app
    app = Flask(__name__)
    config = configparser.ConfigParser()

    config.read(os.path.abspath(os.path.join(".ini")))

    # config.read("/var/www/pia-lara/.ini")
    # config.read(".ini")

    app.config["PIALARA_DB_URI"] = config["LOCAL"]["PIALARA_DB_URI"]
    app.config["PIALARA_DB_NAME"] = config["LOCAL"]["PIALARA_DB_NAME"]
    app.config["SECRET_KEY"] = config["LOCAL"]["SECRET_KEY"]

    app.config["AWS_ACCESS_KEY_ID"] = config["LOCAL"]["AWS_ACCESS_KEY_ID"]
    app.config["AWS_SECRET_ACCESS_KEY"] = config["LOCAL"]["AWS_SECRET_ACCESS_KEY"]
    app.config["BUCKET_NAME"] = config["LOCAL"]["BUCKET_NAME"]

    app.config["GRADIO_URL"] = config["LOCAL"]["GRADIO_URL"]

    # Aplicar Proxy Fix para que Flask reconozca correctamente la IP del cliente y el esquema
    # (http/https) cuando se ejecuta detrás de un proxy inverso como Nginx o Cloudflare
    # x_for=1 significa que confías en el ÚLTIMO proxy de la cadena
    # (el Nginx o Cloudflare directamente delante de Flask)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)  # type: ignore

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    limiter.init_app(app)

    principals = Principal()
    principals.init_app(app)

    # Blueprints
    from pialara.blueprints import audios, auth, lara, main, syllabus, users

    app.register_blueprint(auth.bp)
    app.register_blueprint(syllabus.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(audios.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(lara.bp)

    # Cargar el usuario actual para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return db.get_user_by_id(user_id)

    # Cargar los roles del usuario en la identidad de Flask-Principal
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user

        if hasattr(current_user, "id"):
            identity.provides.add(UserNeed(current_user.get_id()))

        if hasattr(current_user, "rol"):
            identity.provides.add(RoleNeed(current_user.rol))

    # Redirigir a la página de inicio de sesión si el usuario no tiene acceso a una página protegida
    @app.errorhandler(403)
    def acceso_denegado(e):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        return redirect(url_for("users.index"))

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify(
            error="Demasiadas solicitudes. Por favor, inténtalo de nuevo más tarde."
        ), 429

    return app
