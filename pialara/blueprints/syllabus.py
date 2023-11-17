import datetime
from bson.objectid import ObjectId
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import current_user, login_required
from pialara.models.Audios import Audios

from pialara.models.Syllabus import Syllabus
from pialara.models.Usuario import Usuario
from pialara.models.Clicks import Clicks

bp = Blueprint('syllabus', __name__, url_prefix='/syllabus')

@bp.route('/')
def index():
    syllabus = Syllabus()
    frases = syllabus.find()


 # Instancia la clase correspondiente, por ejemplo, Audios
    audios_model = Audios()  # Asegúrate de que Audios sea la clase que hereda de MongoModel

    # Define el pipeline de agregación
    pipeline = [
        {
            '$group': {
                '_id': '$texto.tag',
                'cantidad': {
                    '$sum': 1
                }
            }
        },
        {
            '$sort': {
                'cantidad': -1
            }
        }
    ]

    # Ejecuta la agregación
    result = audios_model.aggregate(pipeline)


    return render_template('syllabus/index.html', syllabus=frases,aggregation_result=result, tag_name='')


@bp.route('/', methods=['POST'])
@login_required
def tag():
    tag_name = request.form.get('tagName')

    if tag_name == "":
        return render_template('syllabus/index.html', syllabus=syllabus.find(), tag_name=tag_name)

    syllabus = Syllabus()
    pipeline = [
        {
            '$unwind': {
                'path': '$tags'
            }
        }, {
            '$match': {
                '$or': [
                    {
                        'tags': {
                            '$regex': tag_name, 
                            '$options': 'i'
                        }
                    }, {
                        'texto': {
                            '$regex': tag_name, 
                            '$options': 'i'
                        }
                    }
                ]
            }
        }
    ]
    frases = syllabus.aggregate(pipeline)

    if not frases.alive:
        flash("No se han encontrado resultados de la etiqueta '" + tag_name + "'", "danger")
 
    # Guardamos el click
    clicks = Clicks()
    click_doc = {
        "class":"syllabus",
        "method":"tag",
        "tag": tag_name,
        "usuario": current_user.email,
        "timestamp": datetime.now()
    }
    clicks.insert_one(click_doc)    

    return render_template('syllabus/index.html', syllabus=frases, tag_name=tag_name)


@bp.route('/create')
@login_required
def create():
    return render_template('syllabus/create.html')


@bp.route('/create', methods=['POST'])
@login_required
def create_post():
    # Obtener los datos del formulario
    text = request.form.get('ftext')
    tags = request.form.get('ftags')

    # Obtener los datos del usuario
    usuario = Usuario()
    params = {"mail": current_user.email}
    user = usuario.find_one(params)

    # Convertir el array de los tags
    tagsArray = tags.split(", ")

    # Crear el texto en la base de datos
    texto = Syllabus()
    aux = {"texto": text, "creador": {"id": user.get("_id"), "nombre": user.get("nombre"), "rol": user.get("rol")},
           "tags": tagsArray, "fecha_creacion": datetime.datetime.now()}
    result = texto.insert_one(aux)

    # Comprobar el resultado y mostrar mensaje
    if result.acknowledged:
        flash('Texto creado correctamente', 'success')
        return redirect(url_for('syllabus.index'))
    else:
        flash('La frase no se ha creado. Error genérico', 'danger')
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
    params2 = {"$set": {"texto": text, "tags": tagsArray}}
    result = texto.update_one(params1, params2, False)

    # Comprobar el resultado y mostrar mensaje
    if result.acknowledged & result.modified_count == 1:
        flash('Texto actualizado correctamente', 'success')
        return redirect(url_for('syllabus.index'))
    elif result.acknowledged & result.modified_count == 0:
        flash('Error al actualizar texto, inténtelo de nuevo...', 'danger')
        return redirect(url_for('syllabus.update', id=fraseID))
    else:
        flash('La frase no se ha actualizado. Error genérico', 'danger')
        return redirect(url_for('syllabus.index'))


@bp.route('/delete/<string:id>')
@login_required
def delete(id):
    frase = Syllabus()
    params = {"_id": ObjectId(id)}
    result = frase.delete_one(params)
    if result.acknowledged:
        flash('Frase eliminada correctamente', 'success')
        return redirect(url_for('syllabus.index'))
    else:
        flash('La frase no se ha eliminado. Error genérico', 'danger')
        return redirect(url_for('syllabus.index'))
