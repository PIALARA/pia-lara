import os.path
import boto3
import random
from bson import ObjectId  # Asegúrate de importar ObjectId desde bson

from bson.objectid import ObjectId
import bson.objectid
from flask import current_app
from flask import Blueprint, render_template
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify, session
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from pialara.models.Audios import Audios
from pialara.models.Frases import Frases
from pialara.models.Usuario import Usuario
from pialara.models.Syllabus import Syllabus
from pialara.models.Clicks import Clicks

from pialara.decorators import rol_required

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
        },
        {
            '$match': {
                'tags': {'$regex': tag_name, '$options': 'i'}
            }
        }
    ]

    # Guardamos el click
    clicks = Clicks()
    click_doc = {
        "class": "audios",
        "method": "client_record",
        "tag": tag_name,
        "usuario": current_user.email,
        "timestamp": datetime.now()
    }
    clicks.insert_one(click_doc)

    # Obtenemos las frases que coinciden con la etiqueta
    syllabus_items = list(syllabus.aggregate(pipeline))  # Convertimos el cursor en lista
    if not syllabus_items:
        flash(f"No se han encontrado frases con la etiqueta '{tag_name}'", "danger")
        return redirect(url_for('audios.client_tag'))  # Redirige si no se encuentran frases
    
    tag_name_ent = session.get('tag_name_ent', None)
   
    if tag_name_ent==tag_name or tag_name_ent==None:
        session['tag_name_ent'] = str(tag_name)
    else:
        session.pop('next_syllabus_item_ent', None) 
        session['tag_name_ent'] = str(tag_name)

    # Recuperamos el id de la siguiente frase desde la sesión (si existe)
    current_item_id = session.get('next_syllabus_item_ent', None)
    next_syllabus_item = None

    if current_item_id:
        # Recuperamos la frase actual
        current_item = syllabus.find_one({"_id": ObjectId(current_item_id)})
        
        if current_item:
            # Comprobamos si tiene el campo 'iterable'
            iterable = current_item.get('iterable', None)
            
            if iterable:
                num = iterable.get('num')
                siguiente_id = iterable.get('siguiente')

                if  num == 1 or siguiente_id!=None:
                    # Si tiene 'iterable.num == 1' y 'siguiente_id', pasamos a la siguiente frase
                    next_syllabus_item = syllabus.find_one({"_id": ObjectId(siguiente_id)})
                    
                    if next_syllabus_item:
                        session['next_syllabus_item_ent'] = str(next_syllabus_item['_id'])
                        
                    else:
                        # Si no tiene 'siguiente_id', seleccionamos aleatoriamente
                        next_syllabus_item = select_random_item(syllabus_items)
                        session['next_syllabus_item_ent'] = str(next_syllabus_item['_id'])
                else:
                    # Si no tiene 'siguiente' o 'iterable.num' no es 1, seleccionamos aleatoria
                    next_syllabus_item = select_random_item(syllabus_items)
                    session['next_syllabus_item_ent'] = str(next_syllabus_item['_id'])
            else:
                # Si no tiene campo 'iterable', seleccionamos aleatoria
                next_syllabus_item = select_random_item(syllabus_items)
                session['next_syllabus_item_ent'] = str(next_syllabus_item['_id'])
        else:
            # Si no se encuentra el item actual, seleccionamos aleatoriamente una frase
            next_syllabus_item = select_random_item(syllabus_items)
            session['next_syllabus_item_ent'] = str(next_syllabus_item['_id'])
    else:
        # Si no hay 'current_item_id', seleccionamos aleatoria
        next_syllabus_item = select_random_item(syllabus_items)
        session['next_syllabus_item_ent'] = str(next_syllabus_item['_id'])

    # Pasamos el item seleccionado a la plantilla
    return render_template('audios/client_record.html', tag=tag_name, syllabus=next_syllabus_item)

# Función para seleccionar una frase aleatoria que no tenga 'iterable' o tenga 'iterable.num = 1'
def select_random_item(syllabus_items):
    # Filtramos las frases que no tienen 'iterable' o tienen 'iterable.num == 1'
    valid_items = [item for item in syllabus_items if not item.get('iterable') or item['iterable'].get('num') == 1]
    if valid_items:
        return random.choice(valid_items)


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

@bp.route('/client-report', methods=['GET'])
@bp.route('/client-report/<id>', methods=['GET'])
@rol_required(['admin', 'tecnico', 'cliente'])
@login_required
def client_report(id=None):
    total_audios = 0
    audios_por_categoria = {}
    logged_rol = current_user.rol
    url = 'audios/client_report.html'
    cliente_nombre = "N/A"

    if id or logged_rol == "cliente":
        audios_model = Audios()
        user_id = ObjectId(id) if id else current_user.id
        
        usuario_model = Usuario()
        cliente = usuario_model.find_one({"_id": user_id})
        cliente_nombre = cliente.get("nombre", "Desconocido") if cliente else "Desconocido"
        
        pipeline = [
            {"$match": {"usuario.id": user_id}},
            {"$group": {"_id": "$texto.tag", "cantidad": {"$sum": 1}}}
        ]
        resultado = list(audios_model.aggregate(pipeline))

        if resultado:
            audios_por_categoria = {doc['_id']: doc['cantidad'] for doc in resultado}
            total_audios = sum(audios_por_categoria.values())
            
    elif logged_rol == "admin":
        audios_model = Audios()
        pipeline = [{"$group": {"_id": "$texto.tag", "cantidad": {"$sum": 1}}}]
        resultado = audios_model.aggregate(pipeline)
        audios_por_categoria = {doc['_id']: doc['cantidad'] for doc in resultado}
        total_audios = sum(audios_por_categoria.values())
        cliente_nombre = "Todos los usuarios"
        
    elif logged_rol == "tecnico":
        usuario_model = Usuario()
        pipeline = [
            {
                "$match": {
                "parent": "tecnico@tecnico.com"
                }
            },
            {
                "$lookup": {
                    "from": "audios",
                    "localField": "_id",
                    "foreignField": "usuario.id",
                    "as": "audios"
                }
            },
            {
                "$unwind": "$audios"
            },
            {
                "$group": {
                    "_id": "$audios.texto.tag",
                    "cantidad": {
                        "$sum": 1
                    }
                }
            }
        ]
        resultado = usuario_model.aggregate(pipeline)
        audios_por_categoria = {doc['_id']: doc['cantidad'] for doc in resultado}
        total_audios = sum(audios_por_categoria.values())
        cliente_nombre = "los Usuarios supervisados"
        
    audios_por_categoria = dict(sorted(audios_por_categoria.items(), key=lambda x: x[1], reverse=True))

    return render_template(url, total_audios=total_audios, audios_por_categoria=audios_por_categoria, usuario_id=id, cliente_nombre=cliente_nombre, rol=logged_rol)
