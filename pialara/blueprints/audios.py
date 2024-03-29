import os.path
import boto3
import random

import bson.objectid
from flask import current_app
from flask import Blueprint, render_template
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from pialara.models.Audios import Audios
from pialara.models.Frases import Frases
from pialara.models.Usuario import Usuario
from pialara.models.Syllabus import Syllabus
from pialara.models.Clicks import Clicks

from datetime import datetime
from random import sample

bp = Blueprint('audios', __name__, url_prefix='/audios')

@bp.route('/client-tag')
@login_required
def client_tag():
    syllabus = Syllabus()
    audio = Audios()

    pipeline = [
        {
            '$unwind': {
                'path': '$tags'
            }
        }, {
            '$group': {
                '_id': '$tags', 
                'fecha': {
                    '$last': '$fecha_creacion'
                }
            }
        }, {
            '$sample': {
                'size': 1
            }
        }
    ]
    tags_suerte = syllabus.aggregate(pipeline)

    # TODO - Es una chapuza ... rehacer en un futuro con una única consulta a MongoDB
    todos_tags = syllabus.distinct("tags",{})
    tags_audios_menos_grabadas = audio.distinct("texto.tag", {"texto.tipo": "syllabus"})
    tags_menos_grabadas = list(set(todos_tags) - set(tags_audios_menos_grabadas))

    if tags_menos_grabadas and len(tags_menos_grabadas) >= 5:
        tags_menos_grabadas = sample(tags_menos_grabadas, 5)
    else:
        tags_menos_grabadas = sample(tags_audios_menos_grabadas, 5)

    tags_aleatorio = sample(list(set(todos_tags)),5)

    return render_template('audios/client_tag.html', tags_suerte=tags_suerte, tags_menos=tags_menos_grabadas, tags3=tags_aleatorio)


@bp.route('/client-record/<string:tag_name>')
@login_required
def client_record(tag_name):
    syllabus = Syllabus()
    pipeline = [
        {
            '$unwind': {
                'path': '$tags'
            }
        }, {
            '$match': {
                'tags': {'$regex': tag_name, '$options': 'i'}
            }
        }
    ]
    syllabus = syllabus.aggregate(pipeline)

    # Guardamos el click
    clicks = Clicks()
    click_doc = {
        "class":"audios",
        "method":"client_record",
        "tag": tag_name,
        "usuario": current_user.email,
        "timestamp": datetime.now()
    }
    clicks.insert_one(click_doc)

    # Obtenemos una frase del syllabus con la etiqueta recibida
    syllabus_list = [syllabus_item for syllabus_item in syllabus]
    random_syllabus = random.choice(syllabus_list)

    # if not frases.alive:
    #     flash("No se han encontrado frases con la etiqueta '" + tag_name + "'", "danger")

    return render_template('audios/client_record.html', tag=tag_name, syllabus=random_syllabus)


@bp.route('/client-text')
@login_required
def client_text():
    return render_template('audios/client_text.html')


@bp.route('/save-record', methods=['POST'])
@login_required
def save_record():
    file = request.files['file']
    duration = request.form.get('duration')

    # print(duration)
    # # Hemos pensado en guardar timestamp + id de usuario. Ver si se guarda en mp3 o wav
    timestamp = int(round(datetime.now().timestamp()))
    filename = str(current_user.id) + '_' + str(timestamp) + '.wav'

    # # Guardado en S3
    s3c = boto3.client(
        's3',
        region_name='eu-south-2',
        aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        # aws_session_token=current_app.config["AWS_SESSION_TOKEN"]
    )

    s3c.upload_fileobj(file, current_app.config["BUCKET_NAME"], filename)

    text_id = request.form.get('text_id')
    text_text = request.form.get('text_text')
    text_tag = request.form.get('text_tag')
    text_type = request.form.get('text_type')

    if text_id:
        # es un texto que proviene de una etiqueta
        print("Viene de una etiqueta")
    else:
        # si no tiene text_id, es un texto grabado por el usuario
        # primero, guardamos el nuevo texto y obtenemos un id
        fraseOb = {
            "texto": text_text,
            "tag": current_user.email,
            "creador": {
                "id": bson.objectid.ObjectId(text_id),
                "mail": current_user.email,
                "nombre": current_user.nombre
            }
        }

        frase = Frases()
        result = frase.insert_one(fraseOb)

        text_id = result.inserted_id

    textoOb = {
        "id": bson.objectid.ObjectId(text_id),
        "texto": text_text,
        "tag": text_tag,
        "tipo": text_type
    }
    usuarioOb = {
        "id": current_user.id,
        "mail": current_user.email, 
        "nombre": current_user.nombre,
        "parent": current_user.parent 
    }
    newAudio = {
        "aws_object_id": filename,
        "usuario": usuarioOb,
        "fecha": datetime.now(),
        "texto": textoOb,
        "duracion": int(duration)
    }
    audio = Audios()
    resultAudio = audio.insert_one(newAudio)

    # Incrementamos en 1 la cantidad de audios grabados
    usuario = Usuario()
    resultUsuario = usuario.update_one({"mail":current_user.email},{"$inc":{"cant_audios":1}})

    data = {
        "status": 'ok',
        "message": "El audio ha sido almacenado correctamente."
    }
    return jsonify(data)

@bp.route('/client-tag', methods=['POST'])
@login_required
def tag_search():
    tag_name = request.form.get('tagName')
    syllabus = Syllabus()

    if tag_name == "":
        return redirect(url_for('audios.client_tag'))

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
        },
        {
            '$group': {
                '_id': '$tags'
            }
        }        
    ]

    tags = syllabus.aggregate(pipeline)

    if not tags.alive:
        flash("No se han encontrado resultados de la etiqueta '" + tag_name + "'", "danger")

    return render_template('audios/client_tag.html', tags=tags, tag_name=tag_name)
