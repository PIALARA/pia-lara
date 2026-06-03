from datetime import datetime
from typing import cast

import pymongo
from bson.objectid import ObjectId
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user as flask_current_user
from flask_login import login_required
from pymongo.errors import PyMongoError
from werkzeug.security import check_password_hash, generate_password_hash

from pialara.models.Disfonias import Disfonias
from pialara.models.Enfermedades import Enfermedades
from pialara.models.User import User
from pialara.models.Usuario import Usuario
from pialara.permissions import admin_o_tecnico

current_user: User = cast(User, flask_current_user)

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/")
@login_required
def index():
    logged_rol = current_user.rol
    url = "users/index.html"

    users = []
    mostrar_inactivos = request.args.get("mostrar_inactivos") == "true"
    u = Usuario()

    if logged_rol == "admin":
        # users = u.find({"activo":True}).sort([("rol", pymongo.ASCENDING), ("nombre", pymongo.ASCENDING)])  # noqa: E501

        if mostrar_inactivos:
            users = u.find({"activo": False}).sort(
                [("rol", pymongo.ASCENDING), ("nombre", pymongo.ASCENDING)]
            )
        else:
            users = u.find({"activo": True}).sort(
                [("rol", pymongo.ASCENDING), ("nombre", pymongo.ASCENDING)]
            )
    elif logged_rol == "tecnico":
        # users = u.find({"rol": {"$eq": 'cliente'}, "parent": { "$eq": current_user.email}})
        if mostrar_inactivos:
            users = u.find(
                {
                    "rol": {"$eq": "cliente"},
                    "parent": {"$eq": current_user.email},
                    "activo": False,
                }
            ).sort([("rol", pymongo.ASCENDING), ("nombre", pymongo.ASCENDING)])
        else:
            users = u.find(
                {
                    "rol": {"$eq": "cliente"},
                    "parent": {"$eq": current_user.email},
                    "activo": True,
                }
            ).sort([("rol", pymongo.ASCENDING), ("nombre", pymongo.ASCENDING)])

    else:
        return redirect(url_for("audios.client_tag"))

    return render_template(url, users=users, user_name="", logged_rol=logged_rol)


@bp.route("/", methods=["POST"])
@login_required
@admin_o_tecnico.require(http_exception=403)
def search_user():
    user_name = request.form.get("userName")
    u = Usuario()

    logged_rol = current_user.rol

    url = "users/index.html"
    if logged_rol == "admin":
        users = u.find({"nombre": {"$regex": user_name, "$options": "i"}})
    else:
        users = u.find(
            {
                "rol": {"$eq": "cliente"},
                "nombre": {"$regex": user_name, "$options": "i"},
                "parent": {"$eq": current_user.email},
            }
        )

    return render_template(url, users=users, user_name=user_name)


@bp.route("/create")
@login_required
@admin_o_tecnico.require(http_exception=403)
def create():
    # u = Usuario()
    logged_rol = current_user.rol

    enfermedades = Enfermedades()
    disfonias = Disfonias()

    return render_template(
        "users/create.html",
        rol=logged_rol,
        enfermedades=enfermedades.find(),
        disfonias=disfonias.find(),
    )


@bp.route("/create", methods=["POST"])
@login_required
@admin_o_tecnico.require(http_exception=403)
def create_post():
    nombreAdmin = request.form.get("nombre_admin")
    emailAdmin = request.form.get("email_admin")
    pass1 = request.form.get("pass1")
    pass2 = request.form.get("pass2")

    nombreTecnico = request.form.get("nombre_tecnico")
    emailTecnico = request.form.get("email_tecnico")

    nombreEntidad = request.form.get("nombre_entidad")
    cifEntidad = request.form.get("cif_entidad")
    personaReferencia = request.form.get("persona_referencia")
    direccionEntidad = request.form.get("direccion_entidad")
    telefonoEntidad = request.form.get("telefono_entidad")
    mailEntidad = request.form.get("mail_entidad")

    nombreTutor = request.form.get("nombre_tutor")
    dniTutor = request.form.get("dni_tutor")
    direccionTutor = request.form.get("direccion_tutor")
    telefonoTutor = request.form.get("telefono_tutor")
    mailTutor = request.form.get("mail_tutor")

    nombreCliente = request.form.get("nombre_cliente")
    dniCliente = request.form.get("dni_cliente")
    fNacCliente = request.form.get("fnac_cliente")
    direccionCliente = request.form.get("direccion_cliente")
    localidadCliente = request.form.get("localidad_cliente")
    provinciaCliente = request.form.get("provincia_cliente")
    sexoCliente = request.form.get("sexo_cliente")
    disCliente = request.form.getlist("dis")
    mailCliente = request.form.get("mail_cliente")
    observacionesCliente = request.form.get("observaciones_cliente")
    enfermedadesCliente = request.form.getlist("enfermedades")
    afectacionCliente = request.form.get("afectacion_cliente")

    user = Usuario()

    if not pass1 or not pass2:
        flash("Las contraseñas no pueden estar vacías", "danger")
        return render_template("users/create.html")

    if len(pass1) < 8:
        flash("La contraseña debe tener al menos 8 caracteres", "danger")
        return render_template("users/create.html")

    if pass1 != pass2:
        flash("Las contraseñas no son iguales", "danger")
        return render_template("users/create.html")

    try:
        # ADMIN
        if nombreAdmin:
            if existeCorreo(emailAdmin):
                flash("El correo del admin ya existe", "danger")
                return redirect(url_for("users.create"))

            newUser = {
                "nombre": nombreAdmin,
                "mail": emailAdmin,
                "rol": "admin",
                "password": generate_password_hash(pass1, method="sha256"),
                "fecha_nacimiento": datetime.now(),
                "ultima_conexion": datetime.now(),
            }
            result = user.insert_one(newUser)

            if result.acknowledged:
                flash("Usuario creado correctamente", "success")
                return redirect(url_for("users.index"))

            flash("El usuario no se ha creado. Error genérico", "danger")
            return redirect(url_for("users.create"))

        # TECNICO
        if nombreTecnico:
            if existeCorreo(emailTecnico):
                flash("El correo del técnico ya existe", "danger")
                return redirect(url_for("users.create"))

            newUser = {
                "nombre": nombreTecnico,
                "mail": emailTecnico,
                "rol": "tecnico",
                "password": generate_password_hash(pass1, method="sha256"),
                "fecha_nacimiento": datetime.now(),
                "ultima_conexion": datetime.now(),
                "activo": True,
            }
            result = user.insert_one(newUser)

            if result.acknowledged:
                flash("Usuario creado correctamente", "success")
                return redirect(url_for("users.index"))

            flash("El usuario no se ha creado. Error genérico", "danger")
            return redirect(url_for("users.create"))

        # CLIENTE
        if nombreCliente:
            if existeCorreo(mailCliente):
                flash("El correo del cliente ya existe", "danger")
                return redirect(url_for("users.create"))

            if not fNacCliente:
                flash("Fecha de nacimiento vacía", "danger")
                return redirect(url_for("users.create"))

            fecha = datetime.strptime(fNacCliente, "%Y-%m-%d")

            newUser = {
                "schema_version": 2,
                "nombre": nombreCliente,
                "mail": mailCliente,
                "rol": "cliente",
                "password": generate_password_hash(pass1, method="sha256"),
                "fecha_nacimiento": fecha,
                "ultima_conexion": datetime.now(),
                "sexo": sexoCliente,
                "provincia": provinciaCliente,
                "parent": current_user.email,
                "perfil": {
                    "entidad": {
                        "nombre": nombreEntidad,
                        "cif": cifEntidad,
                        "persona_referencia": personaReferencia,
                        "direccion": direccionEntidad,
                        "telefono": telefonoEntidad,
                        "mail": mailEntidad,
                        "colectivos_atencion": enfermedadesCliente,
                    },
                    "tutor": {
                        "nombre": nombreTutor,
                        "dni": dniTutor,
                        "direccion": direccionTutor,
                        "telefono": telefonoTutor,
                        "mail": mailTutor,
                    },
                    "participante": {
                        "nombre": nombreCliente,
                        "dni": dniCliente,
                        "fecha_nacimiento": fecha,
                        "direccion": direccionCliente,
                        "localidad": localidadCliente,
                        "provincia": provinciaCliente,
                        "sexo": sexoCliente,
                        "trastornos_habla": disCliente,
                        "grado_afectacion": afectacionCliente,
                    },
                    "observaciones": observacionesCliente,
                },
                "font_size": 1,
                "cant_audios": 0,
                "activo": True,
            }

            result = user.insert_one(newUser)

            if result.acknowledged:
                flash("Usuario creado correctamente", "success")
                return redirect(url_for("users.index"))

            flash("El usuario no se ha creado. Error genérico", "danger")
            return redirect(url_for("users.create"))

        # Si no venía nada que crear
        flash("Formulario incompleto: no se recibió admin/técnico/cliente", "danger")
        return redirect(url_for("users.create"))

    except PyMongoError as e:
        flash(f"Error MongoDB: {str(e)}", "danger")
        return redirect(url_for("users.create"))

    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("users.create"))


def existeCorreo(email):
    user = Usuario()
    aux = user.count_documents({"mail": email})
    if aux > 0:
        return True

    return False


@bp.route("/update-tech/<id>", methods=["GET"])
@login_required
def update_tech(id):
    u = Usuario()
    model = u.find_one({"_id": ObjectId(id)})

    # Guardamos todos los tecnicos
    tecnicos = u.find({"rol": "tecnico"})

    return render_template("users/update-tech.html", user=model, tecnicos=tecnicos)


@bp.route("/update-tech/<id>", methods=["POST"])
@login_required
def update_tech_post(id):
    usu = Usuario()
    tecnico = request.form.get("tecnico")

    if not tecnico or len(tecnico) != 24:
        flash("Error localizando al técnico. Id inexistente.", "danger")
        return redirect(url_for("users.index"))

    # Guardamos en model_tec el tecnico seleccionado
    model_tec = usu.find_one({"_id": ObjectId(tecnico)})

    # Creamos la variable mail para guardar el correo del tecnico
    mail = ""

    # Comprobamos si existe el id recogido en el formulario
    if model_tec:
        # Si funciona, guardamos su correo
        mail = model_tec.get("mail")
    else:
        # Si no lo encuentra, cancelamos la operacion y avisamos del error
        flash("Error localizando al técnico seleccionado", "danger")
        return redirect(url_for("users.index"))

    mongo_set = {"$set": {"parent": mail}}

    print("MONGO_SET", mongo_set)
    # resultado = usu.update_one({"_id": ObjectId(id)}, mongo_set)
    usu.update_one({"_id": ObjectId(id)}, mongo_set)

    flash("Tecnico migrado con exito", "success")
    return redirect(url_for("users.index"))


@bp.route("/update", defaults={"id": None}, methods=["GET"])
@bp.route("/update/<id>", methods=["GET"])
@login_required
def update(id: str | None):
    if not id:
        id = str(current_user.id)

    usu = Usuario()

    if current_user.rol != "admin" and current_user.rol != "tecnico" and str(current_user.id) != id:
        flash("No tienes permiso para editar este usuario", "danger")
        return redirect(url_for("users.index"))

    # Usuario a actualizar
    usuario = usu.find_one({"_id": ObjectId(id)})

    # Rol del usuario logeado
    logged_rol = current_user.rol

    # Datos auxiliares, incluye datos que necesite la plantilla
    datos_aux = {}

    if usuario["rol"] == "admin":
        url = "users/update-admin.html"
    elif usuario["rol"] == "tecnico":
        url = "users/update-tecnico.html"
    else:
        datos_aux["enfermedades"] = Enfermedades().find()
        datos_aux["disfonias"] = Disfonias().find()
        datos_aux["provincias"] = [
            "Álava",
            "Albacete",
            "Alicante",
            "Almería",
            "Asturias",
            "Ávila",
            "Badajoz",
            "Barcelona",
            "Burgos",
            "Cáceres",
            "Cádiz",
            "Cantabria",
            "Castellón",
            "Ciudad Real",
            "Córdoba",
            "Cuenca",
            "Girona",
            "Granada",
            "Guadalajara",
            "Guipúzcoa",
            "Huelva",
            "Huesca",
            "Islas Baleares",
            "Jaén",
            "La Coruña",
            "La Rioja",
            "Las Palmas",
            "León",
            "Lleida",
            "Lugo",
            "Madrid",
            "Málaga",
            "Murcia",
            "Navarra",
            "Ourense",
            "Palencia",
            "Pontevedra",
            "Salamanca",
            "Santa Cruz de Tenerife",
            "Segovia",
            "Sevilla",
            "Soria",
            "Tarragona",
            "Teruel",
            "Toledo",
            "Valencia",
            "Valladolid",
            "Vizcaya",
            "Zamora",
            "Zaragoza",
        ]
        url = "users/update.html"

    return render_template(url, model=usuario, rol=logged_rol, datos_aux=datos_aux)


# Actualiza datos de usuarios - POST
@bp.route("/update", defaults={"id": None}, methods=["POST"])
@bp.route("/update/<id>", methods=["POST"])
@login_required
def update_post(id: str | None):
    if not id:
        id = str(current_user.id)

    usu = Usuario()
    usuario_db = usu.find_one({"_id": ObjectId(id)})

    if not usuario_db:
        flash("Usuario no encontrado", "danger")
        return redirect(url_for("users.index"))

    rol_usuario_objetivo = usuario_db.get("rol")
    schema_version = str(request.form.get("schema_version", "1"))

    font_size = request.form.get("font_size", 1) or 1

    activo = True if request.form.get("activo") else False

    rol_editor = current_user.rol
    puede_editar_restringido = rol_editor in ("admin", "tecnico")

    # ========== SCHEMA VERSION 2 ==========
    if schema_version == "2":
        email = request.form.get("email")
        sexo = request.form.get("sexo")
        provincia = request.form.get("provincia")
        observaciones = request.form.get("observaciones")

        nombre_cliente = request.form.get("nombre_cliente")
        dni_cliente = request.form.get("dni_cliente")
        fnac_cliente = request.form.get("fnac_cliente")
        direccion_cliente = request.form.get("direccion_cliente")
        localidad_cliente = request.form.get("localidad_cliente")
        telefono_cliente = request.form.get("telefono_cliente")

        fecha_cliente = None
        if fnac_cliente:
            fecha_cliente = datetime.strptime(fnac_cliente, "%Y-%m-%d")

        mongo_set = {
            "$set": {
                "schema_version": 2,
                "nombre": nombre_cliente,
                "mail": email,
                "sexo": sexo,
                "provincia": provincia,
                "fecha_nacimiento": fecha_cliente
                if fecha_cliente
                else usuario_db.get("fecha_nacimiento"),
                "activo": activo,
                "font_size": float(font_size),
                "perfil.participante.nombre": nombre_cliente,
                "perfil.participante.dni": dni_cliente,
                "perfil.participante.fecha_nacimiento": fecha_cliente
                if fecha_cliente
                else usuario_db.get("fecha_nacimiento"),
                "perfil.participante.direccion": direccion_cliente,
                "perfil.participante.localidad": localidad_cliente,
                "perfil.participante.provincia": provincia,
                "perfil.participante.sexo": sexo,
                "perfil.participante.telefono": telefono_cliente,
                "perfil.observaciones": observaciones,
            }
        }

        if puede_editar_restringido:
            nombre_entidad = request.form.get("nombre_entidad")
            cif_entidad = request.form.get("cif_entidad")
            persona_referencia = request.form.get("persona_referencia")
            direccion_entidad = request.form.get("direccion_entidad")
            telefono_entidad = request.form.get("telefono_entidad")
            mail_entidad = request.form.get("mail_entidad")
            colectivos_atencion = request.form.getlist("enfermedades")

            nombre_tutor = request.form.get("nombre_tutor")
            dni_tutor = request.form.get("dni_tutor")
            direccion_tutor = request.form.get("direccion_tutor")
            telefono_tutor = request.form.get("telefono_tutor")
            mail_tutor = request.form.get("mail_tutor")

            trastornos_habla = request.form.getlist("disfonia")
            grado_afectacion = request.form.get("afectacion_cliente")

            mongo_set["$set"].update(
                {
                    "perfil.entidad.nombre": nombre_entidad,
                    "perfil.entidad.cif": cif_entidad,
                    "perfil.entidad.persona_referencia": persona_referencia,
                    "perfil.entidad.direccion": direccion_entidad,
                    "perfil.entidad.telefono": telefono_entidad,
                    "perfil.entidad.mail": mail_entidad,
                    "perfil.entidad.colectivos_atencion": colectivos_atencion,
                    "perfil.tutor.nombre": nombre_tutor,
                    "perfil.tutor.dni": dni_tutor,
                    "perfil.tutor.direccion": direccion_tutor,
                    "perfil.tutor.telefono": telefono_tutor,
                    "perfil.tutor.mail": mail_tutor,
                    "perfil.participante.trastornos_habla": trastornos_habla,
                    "perfil.participante.grado_afectacion": grado_afectacion,
                }
            )

        resultado = usu.update_one({"_id": ObjectId(id)}, mongo_set)

        if resultado.acknowledged:
            session["font_size"] = font_size
            flash("Usuario actualizado correctamente", "success")
            return redirect(url_for("users.index", id=id))

        flash("Error al actualizar el usuario, inténtelo de nuevo...", "danger")
        return redirect(url_for("users.update", id=id))

    # ========== SCHEMA VERSION 1 ==========
    nombre = request.form.get("nombre_cliente") or request.form.get("nombre")
    email = request.form.get("email")
    sexo = request.form.get("sexo")
    provincia = request.form.get("provincia")
    entidad = request.form.get("entidad")
    fnac = request.form.get("fnac_cliente") or request.form.get("fnac")
    observaciones = request.form.get("observaciones")

    fecha = None
    if fnac:
        fecha = datetime.strptime(fnac, "%Y-%m-%d")

    mongo_set = {
        "$set": {
            "nombre": nombre,
            "mail": email,
            "sexo": sexo,
            "provincia": provincia,
            "activo": activo,
            "observaciones": observaciones,
            "fecha_nacimiento": fecha if fecha else usuario_db.get("fecha_nacimiento"),
            "font_size": float(font_size),
        }
    }

    if puede_editar_restringido:
        mongo_set["$set"]["entidad"] = entidad

    if rol_usuario_objetivo == "cliente" and puede_editar_restringido:
        enfermedades = request.form.getlist("enfermedades")
        disfonias = request.form.getlist("disfonia")
        mongo_set["$set"]["enfermedades"] = enfermedades
        mongo_set["$set"]["dis"] = disfonias

    resultado = usu.update_one({"_id": ObjectId(id)}, mongo_set)

    if resultado.acknowledged:
        session["font_size"] = font_size
        flash("Usuario actualizado correctamente", "success")
        return redirect(url_for("users.index", id=id))

    flash("Error al actualizar el usuario, inténtelo de nuevo...", "danger")
    return redirect(url_for("users.update", id=id))


# Actualizar Contraseña - GET
@bp.route("/update-pass/<id>", methods=["GET"])
@login_required
def update_pass_get(id):
    usu = Usuario()

    # Usuario a actualizar
    usuario = usu.find_one({"_id": ObjectId(id)})

    # Usuario logeado
    logged_user = current_user

    return render_template("users/update-pass.html", model=usuario, logged_usuario=logged_user)


# Actualizar Contraseña - POST
@bp.route("/update-pass/<id>", methods=["POST"])
@login_required
def update_pass_post(id):
    usu = Usuario()

    # Usuario a actualizar
    # usuario = usu.find_one({"_id": ObjectId(id)})

    # Usuario logeado
    logged_user = current_user

    user_logged_pass = request.form.get("pass")
    new_pass = request.form.get("new-pass")
    repeat_pass = request.form.get("repeat-pass")

    # Comprobar Password usuario
    if not user_logged_pass or not check_password_hash(logged_user.password, user_logged_pass):
        flash("Su contraseña no es correcta", "danger")
        return redirect(url_for("users.update_pass_post", id=id))

    # Comprobar nueva Password
    if not new_pass or not repeat_pass:
        flash("Las contraseñas no pueden estar vacías", "danger")
        return redirect(url_for("users.update_pass_post", id=id))

    if len(new_pass) < 8:
        flash("La nueva contraseña debe tener al menos 8 caracteres", "danger")
        return redirect(url_for("users.update_pass_post", id=id))

    if new_pass != repeat_pass:
        flash("Las contraseñas no son iguales", "danger")
        return redirect(url_for("users.update_pass_post", id=id))

    mongo_set = {"$set": {"password": generate_password_hash(new_pass, method="sha256")}}

    # Actualizar en BD
    resultado = usu.update_one({"_id": ObjectId(id)}, mongo_set)

    # Mensajes de salida
    if resultado.acknowledged:
        flash("Contraseña actualizada correctamente", "success")
        return redirect(url_for("users.index"))
    else:
        flash("Error al actualizar la constraseña, inténtelo de nuevo...", "danger")
        return redirect(url_for("users.update_pass_post", id=id))


@bp.route("/consent")
@login_required
def consent():
    # logged_rol = current_user.rol
    login_url = url_for("users.index")

    # if logged_rol == 'cliente':
    #    login_url = url_for('audios.client_tag')

    return render_template("users/consent.html", login_url=login_url)
