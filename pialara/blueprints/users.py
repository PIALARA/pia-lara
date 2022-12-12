from datetime import datetime
from urllib import request

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, current_user
from pialara.db import db
from pialara.models.Usuario import Usuario
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from pialara.models.MongoModel import MongoModel as mongo

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/')
@login_required
def index():
    u = Usuario()

    # logged_rol = current_user.rol
    # if logged_rol == "Administrador":
    #     users = db.users.find()
    # else:
    #     raise Exception("Operación no permitida para el rol", logged_rol)

    return render_template('users/index.html', users=u.find())


@bp.route('/create')
@login_required
def create():
    return render_template('users/create.html')

@bp.route('/create', methods=['POST'])
@login_required
def create_post():
    nombreAdmin = request.form.get('nombre_admin')
    emailAdmin = request.form.get('email_admin')
    pass1 = request.form.get('pass1')
    pass2 = request.form.get('pass2')

    nombreTecnico = request.form.get('nombre_tecnico')
    emailTecnico = request.form.get('email_tecnico')

    nombreCliente = request.form.get('nombre_cliente')
    emailCliente = request.form.get('email_cliente')
    fNacCliente = request.form.get('fnac_cliente')
    sexoCliente = request.form.get('sexo_cliente')
    provinciaCliente = request.form.get('provincia_cliente')
    enfermedadesCliente = request.form.getlist('enfermedades')
    disCliente = request.form.getlist('dis')

    user = Usuario()

    if pass1 != pass2:
        flash("Las contraseñas no son iguales")
        return render_template('users/create.html')


    result = None

    if nombreAdmin and not existeCorreo(emailAdmin):

        newUser = {"nombre": nombreAdmin, "mail": emailAdmin, "rol": "admin",
                   "password": generate_password_hash(pass1, method='sha256'),
                   "fecha_nacimiento":datetime.now(), "ultima_conexion":datetime.now()}
        result = user.insert_one(newUser)

    elif nombreTecnico and not existeCorreo(emailTecnico):
        newUser = {"nombre": nombreTecnico, "mail": emailTecnico, "rol": "tecnico",
                   "password": generate_password_hash(pass1, method='sha256'),
                   "fecha_nacimiento": datetime.now(), "ultima_conexion": datetime.now()}
        result = user.insert_one(newUser)

    elif nombreCliente and not existeCorreo(emailCliente):
        fecha = datetime.strptime(fNacCliente, '%Y-%m-%d')
        newUser = {"nombre": nombreCliente, "mail": emailCliente, "rol": "cliente",
                   "password": generate_password_hash(pass1, method='sha256'),
                   "fecha_nacimiento": fecha, "ultima_conexion": datetime.now(),
                   "sexo": sexoCliente, "provincia": provinciaCliente,
                   "enfermedades": enfermedadesCliente, "dis": disCliente,
                   }
        result = user.insert_one(newUser)


    # Comprobar el resultado y mostrar mensaje
    if not result == None and result.acknowledged:
        flash('Usuario creado correctamente', 'success')
        return redirect(url_for('users.index'))
    else:
        flash('El usuario no se ha creado. Error genérico', 'danger')
        return redirect(url_for('users.create'))


def existeCorreo(email):
    user = Usuario()
    aux = user.count_documents({'mail': email})
    if aux > 0:
        return True

    return False

@bp.route('/update/<id>', methods=['GET'])
@login_required
def update(id):
    u = Usuario()
    model=u.find_one({'_id': ObjectId(id)})
   
    return render_template('users/update.html',model=model)

@bp.route('/update/<id>', methods=['POST'])
@login_required
def update_post(id):
    usu = Usuario()
    nombre = request.form.get('nombre')
    email = request.form.get('email')
  
    resultado = usu.update_one({'_id': ObjectId(id)},{"$set":{'nombre':nombre, 'mail':email}})
    if resultado.acknowledged & resultado.modified_count == 1:
        flash('Usuario actualizado correctamente')
        return redirect(url_for('users.index'))
    elif resultado.acknowledged & resultado.modified_count == 0:
        flash('Error al actualizar el usuario, inténtelo de nuevo...')
        return redirect(url_for('users.update', id=id))
    else:
        flash('La usuario no se ha actualizado. Error genérico')
        return redirect(url_for('users.index'))


"""
@bp.route('/update', methods=['POST'])
@login_required
def updateData():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    password = request.form.get('password')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    sexo = request.form.get('sexo')
    provincia = request.form.get('provincia')
    enfermedades = request.form.get('enfermedades')
    dis = request.form.get('dis')

    result = db.update_user_all()
    print("Usuario modificado: ",result)
"""
"""@bp.route('/update/<id>', methods=['GET'])
@login_required
def update(id):
    u = Usuario()
    model=u.find_one({'_id': ObjectId(id)})
    if model is None:
        flash("usuario no existe", "error")
        return render_template('users/index.html')

    return render_template('users/update.html',model=model)"""


