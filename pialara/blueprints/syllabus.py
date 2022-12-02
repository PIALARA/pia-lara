import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from pialara.models.Syllabus import Syllabus
from pialara.models.Usuario import Usuario
from bson.objectid import ObjectId
from flask_login import current_user, login_required

bp = Blueprint('syllabus', __name__, url_prefix='/syllabus')

from pialara.db import get_db


@bp.route('/')
def index():
    return render_template('syllabus/index.html')


@bp.route('/create')
@login_required
def create():
    return render_template('syllabus/create.html')


@bp.route('/create', methods=['POST'])
@login_required
def create_post():
    #Obtener los datos del formulario
    text = request.form.get('ftext')
    tags = request.form.get('ftags')

    #Obtener los datos del usuario
    usuario = Usuario()
    params = {"mail": current_user.email}
    user = usuario.find_one(params)


    #Convertir el array de los tags
    tagsArray = tags.split(", ")

    #Crear el texto en la base de datos
    texto = Syllabus()
    aux = {"texto": text, "creador": {"id": user.get("_id"), "nombre": user.get("nombre"), "rol": user.get("rol")}, "tags": tagsArray, "fecha_creacion": datetime.datetime.now()}
    result = texto.insert_one(aux)

    #Comprobar el resultado y mostrar mensaje
    if result.acknowledged:
        flash('Texto creado correctamente')
        return redirect(url_for('syllabus.index'))
    else:
        flash('La frase no se ha creado. Error genérico')
        return redirect(url_for('syllabus.create'))



@bp.route('/update/<string:id>')
@login_required
def update(id):
    frase = Syllabus()
    params = {"_id": ObjectId(id)}
    syllabus = frase.find_one(params)

    aux = ""
    tags = syllabus.get('tags')
    for x in tags:
        aux = aux + ", " + x

    aux = aux[2:]

    return render_template('syllabus/update.html', syllabus=syllabus, tags=aux)

@bp.route('/update/<string:id>', methods=['POST'])
@login_required
def update_post(id):
    # Obtener los datos del formulario
    text = request.form.get('ftext')
    tags = request.form.get('ftags')
    fraseID = id

    # Obtener los datos del usuario
    usuario = Usuario()
    params = {"email": current_user.email}
    user = usuario.find_one(params)

    # Convertir el array de los tags
    tagsArray = tags.split(", ")

    # Crear el texto en la base de datos
    texto = Syllabus()
    params1 = {"_id": ObjectId(fraseID)}
    params2 = {"$set":  {"texto": text, "tags": tagsArray}}
    result = texto.update_one(params1, params2, False)

    # Comprobar el resultado y mostrar mensaje
    if result.acknowledged & result.modified_count == 1:
        flash('Texto actualizado correctamente')
        return redirect(url_for('syllabus.index'))
    elif result.acknowledged & result.modified_count == 0:
        flash('Error al actualizar texto, inténtelo de nuevo...')
        return redirect(url_for('syllabus.update', id=fraseID))
    else:
        flash('La frase no se ha actualizado. Error genérico')
        return redirect(url_for('syllabus.index'))



"""
@bp.route('/update/:id')
def update():
    return render_template('syllabus/update.html')

@bp.route('/update/:id', methods=['post'])
def update_post():
    flash('modificado correctamente')
    redirect('/update')


@bp.route('/delete/:id')
def delete():
    return render_template('syllabus/index.html')

@bp.route('/view/:id')
def view():
    return render_template('syllabus/index.html')
"""
