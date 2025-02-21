from werkzeug.security import generate_password_hash

from datetime import datetime
from bson.objectid import ObjectId
import pymongo
from flask import Blueprint, render_template, request
from urllib import request

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flask_login import login_required, current_user
from pialara.decorators import rol_required
from pialara.models.Usuario import Usuario
from pialara.models.Enfermedades import Enfermedades
from pialara.models.Disfonias import Disfonias
from pialara.decorators import rol_required

from werkzeug.security import check_password_hash
from pialara import db

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/')
@login_required
@rol_required(['admin', 'tecnico', 'cliente'])
def index():
	# mostrar_inactivos=request.form.get("mostrar_inactivos")
    mostrar_inactivos = request.args.get('mostrar_inactivos') == 'true'
    u = Usuario()

    users = []
    logged_rol = current_user.rol
    url = 'users/index.html'

    if logged_rol == "admin":
        # users = u.find({"activo":True}).sort([("rol", pymongo.ASCENDING), ("nombre", pymongo.ASCENDING)])
		
        if mostrar_inactivos:
            users = u.find({"activo": False}).sort([("rol", pymongo.ASCENDING), ("nombre", pymongo.ASCENDING)])
        else:
            users = u.find({"activo": True}).sort([("rol", pymongo.ASCENDING), ("nombre", pymongo.ASCENDING)])
    elif logged_rol == "tecnico":

        # users = u.find({"rol": {"$eq": 'cliente'}, "parent": { "$eq": current_user.email}})
        if mostrar_inactivos:
            users = u.find({"rol": {"$eq": 'cliente'}, "parent": {"$eq": current_user.email}, "activo": False}).sort([("rol", pymongo.ASCENDING), ("nombre", pymongo.ASCENDING)])
        else:
            users = u.find({"rol": {"$eq": 'cliente'}, "parent": {"$eq": current_user.email}, "activo": True}).sort([("rol", pymongo.ASCENDING), ("nombre", pymongo.ASCENDING)])
    							 
																																												 
			 
																																												
    else:
        return redirect(url_for('audios.client_tag'))
	

    return render_template(url, users=users, user_name='', logged_rol=logged_rol)


@bp.route('/', methods=['POST'])
@login_required
@rol_required(['admin', 'tecnico'])
def search_user():
    user_name = request.form.get('userName')
    u = Usuario()

    logged_rol = current_user.rol

    url = 'users/index.html'
    if logged_rol == "admin":
        users = u.find({'nombre': {"$regex": user_name, '$options': 'i'}})
    else:
        users = u.find({"rol": {"$eq": 'cliente'}, 'nombre': {
                       "$regex": user_name, '$options': 'i'}, "parent": {"$eq": current_user.email}})

    return render_template(url, users=users, user_name=user_name)


@bp.route('/create')
@login_required
@rol_required(['admin', 'tecnico'])
def create():
    u = Usuario()
    logged_rol = current_user.rol

    enfermedades = Enfermedades()
    disfonias = Disfonias()

    return render_template(
        'users/create.html',
        rol=logged_rol,
        enfermedades=enfermedades.find(),
        disfonias=disfonias.find()
    )


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
    activoCliente = request.form.get('activo_cliente')												  
    emailCliente = request.form.get('email_cliente')
    fNacCliente = request.form.get('fnac_cliente')
    sexoCliente = request.form.get('sexo_cliente')
    provinciaCliente = request.form.get('provincia_cliente')
    entidadCliente = request.form.get('entidad_cliente')
    observacionesCliente = request.form.get('observaciones_cliente')
    enfermedadesCliente = request.form.getlist('enfermedades')
    disCliente = request.form.getlist('dis')

    user = Usuario()

    if pass1 != pass2:
        flash("Las contraseñas no son iguales", 'danger')
        return render_template('users/create.html')

    result = None

    if nombreAdmin and not existeCorreo(emailAdmin):

        newUser = {"nombre": nombreAdmin, "mail": emailAdmin, "rol": "admin",
                   "password": generate_password_hash(pass1, method='sha256'),
                   "fecha_nacimiento": datetime.now(), "ultima_conexion": datetime.now()}
        result = user.insert_one(newUser)

    elif nombreTecnico and not existeCorreo(emailTecnico):
        newUser = {"nombre": nombreTecnico, "mail": emailTecnico, "rol": "tecnico",
                   "password": generate_password_hash(pass1, method='sha256'),
                   "fecha_nacimiento": datetime.now(), "ultima_conexion": datetime.now(),
                   "activo": True}
        result = user.insert_one(newUser)

    elif nombreCliente and not existeCorreo(emailCliente):
        fecha = datetime.strptime(fNacCliente, '%Y-%m-%d')
        newUser = {"nombre": nombreCliente, "mail": emailCliente, "rol": "cliente",
                   "password": generate_password_hash(pass1, method='sha256'),
                   "fecha_nacimiento": fecha, "ultima_conexion": datetime.now(),
                   "sexo": sexoCliente, "provincia": provinciaCliente, "entidad": entidadCliente,
                   "observaciones": observacionesCliente,
                   "enfermedades": enfermedadesCliente, "dis": disCliente,
                   "parent": current_user.email, "cant_audios": 0,
                   "activo": True}
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


@bp.route('/update-tech/<id>', methods=['GET'])
@login_required
def update_tech(id):
    u = Usuario()
    model = u.find_one({'_id': ObjectId(id)})

    # Guardamos todos los tecnicos
    tecnicos = u.find({'rol': 'tecnico'})


    return render_template('users/update-tech.html', user=model, tecnicos=tecnicos)

@bp.route('/update-tech/<id>', methods=['POST'])
@login_required
def update_tech_post(id):
    usu = Usuario()
    tecnico = request.form.get('tecnico')

    if len(tecnico) != 24:
        flash('Error localizando al técnico. Id inexistente.', 'danger')
        return redirect(url_for('users.index'))

    # Guardamos en model_tec el tecnico seleccionado
    model_tec = usu.find_one({'_id': ObjectId(tecnico)})

    # Creamos la variable mail para guardar el correo del tecnico
    mail = ""

    # Comprobamos si existe el id recogido en el formulario
    if model_tec:

        # Si funciona, guardamos su correo
        mail = model_tec.get('mail')
    else:

        # Si no lo encuentra, cancelamos la operacion y avisamos del error
        flash('Error localizando al técnico seleccionado', 'danger')
        return redirect(url_for('users.index'))


    mongo_set = {"$set": {'parent': mail}}

    print("MONGO_SET", mongo_set)
    resultado = usu.update_one({'_id': ObjectId(id)}, mongo_set)

    flash('Tecnico migrado con exito', 'success')
    return redirect(url_for('users.index'))



@bp.route('/update/<id>', methods=['GET'])
@login_required
def update(id):
    usu = Usuario()

    # Usuario a actualizar
    usuario = usu.find_one({'_id': ObjectId(id)})

    # Rol del usuario logeado
    logged_rol = current_user.rol
 
    # Datos auxiliares, incluye datos que necesite la plantilla
    datos_aux ={} 
 
    if usuario['rol'] == 'admin':
        url = 'users/update-admin.html'
    elif usuario['rol'] == 'tecnico':
        url = 'users/update-tecnico.html'
    else:
        datos_aux["enfermedades"] = Enfermedades().find()
        datos_aux["disfonias"] = Disfonias().find()
        datos_aux["provincias"] = ['Alicante','Valencia','Castellon','Murcia']
        url = 'users/update.html'
        
    return render_template( url, model=usuario, rol=logged_rol, datos_aux=datos_aux )


# Actualiza datos de usuarios - POST
@bp.route('/update/<id>', methods=['POST'])
@login_required
def update_post(id):
    usu = Usuario()

    # Rol del usuario a actualizar
    rol_usuario = usu.find_one({'_id': ObjectId(id)})['rol']
    
    nombre = request.form.get('nombre')
									   
    email = request.form.get('email')
    sexo = request.form.get('sexo')
    provincia = request.form.get('provincia')
    entidad = request.form.get('entidad')
    fnac = request.form.get('fnac')
    observaciones = request.form.get('observaciones')
    font_size = request.form.get('font_size', 1)
    enfermedades = request.form.getlist('enfermedad')
    disfonias = request.form.getlist('disfonia')
    activo = request.form.get('activo')
    fecha = datetime.strptime(fnac, '%Y-%m-%d')

    activo = True if activo else False

    if not font_size:
        font_size = 1

    mongo_set = {"$set": {'nombre': nombre, 'mail': email, 'sexo': sexo, 'provincia': provincia, 
                          'entidad': entidad, 'activo': activo,'observaciones': observaciones,
                          'fecha_nacimiento': fecha , 'font_size': float(font_size)}}
    
    # Añadir atributos especificos de cliente
    if rol_usuario == "cliente":
         mongo_set["$set"]["enfermedades"] = enfermedades
         mongo_set["$set"]["dis"] = disfonias
   
    # Actualizar en BD
    resultado = usu.update_one({'_id': ObjectId(id)}, mongo_set)
 
    if resultado.acknowledged:
        session['font_size'] = font_size
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('users.index', id=id))
    else:
        flash('Error al actualizar el usuario, inténtelo de nuevo...', 'danger')

    return redirect(url_for('users.update', id=id))


# Actualizar Contraseña - GET
@bp.route('/update-pass/<id>', methods=['GET'])
@login_required
def update_pass_get(id):
    usu = Usuario()

    # Usuario a actualizar
    usuario = usu.find_one({'_id': ObjectId(id)})

    # Usuario logeado
    logged_user = current_user

    return render_template('users/update-pass.html', model=usuario, logged_usuario=logged_user)


# Actualizar Contraseña - POST
@bp.route('/update-pass/<id>', methods=['POST'])
@login_required
def update_pass_post(id):
    usu = Usuario()

    # Usuario a actualizar
    usuario = usu.find_one({'_id': ObjectId(id)})

    # Usuario logeado
    logged_user = current_user

    user_logged_pass = request.form.get('pass')
    new_pass = request.form.get('new-pass')
    repeat_pass = request.form.get('repeat-pass')

    # Comprobar Password usuario
    if not check_password_hash(logged_user.password, user_logged_pass):
        flash("Su contraseña no es correcta", 'danger')
        return redirect(url_for('users.update_pass_post', id=id))
    
    # Comprobar nueva Password
    if new_pass != repeat_pass:
        flash("Las contraseñas no son iguales", 'danger')
        return redirect(url_for('users.update_pass_post', id=id))

    mongo_set = {"$set": {'password': generate_password_hash(new_pass, method='sha256')}}

    # Actualizar en BD
    resultado = usu.update_one({'_id': ObjectId(id)}, mongo_set)

    # Mensajes de salida
    if resultado.acknowledged:
        flash('Contraseña actualizada correctamente', 'success')
        return redirect(url_for('users.index'))
    else:
        flash('Error al actualizar la constraseña, inténtelo de nuevo...', 'danger')
        return redirect(url_for('users.update_pass_post', id=id))
     
    

@bp.route('/consent')
@login_required
def consent():
    logged_rol = current_user.rol
    login_url = url_for('users.index')

    # if logged_rol == 'cliente':
    #    login_url = url_for('audios.client_tag')

    return render_template('users/consent.html', login_url=login_url)
