import os.path
import boto3
import random
import re
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

@bp.route('/cliente-tag')
@login_required
def client_tag():
    audio = Audios()
    
    match_base = {
        "texto.tipo": "syllabus",
        "usuario.mail": current_user.email
    }

    pipeline = [
        {"$match": match_base},
        {
            "$facet": {
                # Cantidad total de audios
                "total_audios": [
                    {"$count": "total"}
                ],
                "totales_por_etiqueta": [
                    {"$group": {"_id": "$texto.tag", "total": {"$sum": 1}}},
                    {"$sort": {"total": -1}},
                    {"$project": {"_id": 0, "tag": "$_id", "total": 1}}
                ],
                # Últimas 5 etiquetas grabadas
                "ultimas_etiquetas": [
                    {"$sort": {"fecha": -1}},
                    {"$limit": 5},
                    {"$project": {"_id": 0, "tag": "$texto.tag", "fecha": 1}}
                ],
                # Cantidad total de fonemas distintos
                "total_fonemas": [
                    {"$match": {"metadata.fonema": {"$exists": True}}},
                    {"$group": {"_id": "$metadata.fonema"}},
                    {"$count": "total"}
                ],

                # Últimos 5 fonemas grabados
                "ultimos_fonemas": [
                    {"$match": {"metadata.fonema": {"$exists": True}}},
                    {"$sort": {"fecha": -1}},
                    {"$group": {"_id": "$metadata.fonema", "last_time": {"$first": "$fecha"}}},
                    {"$sort": {"last_time": -1}},
                    {"$limit": 5},
                    {"$project": {"_id": 0, "fonema": "$_id", "fecha": "$last_time"}}
                ],

                # 5 fonemas más grabados
                "top_fonemas": [
                    {"$match": {"metadata.fonema": {"$exists": True}}},
                    {"$group": {"_id": "$metadata.fonema", "total": {"$sum": 1}}},
                    {"$sort": {"total": -1}},
                    {"$limit": 5},
                    {"$project": {"_id": 0, "fonema": "$_id", "total": 1}}
                ],

                # 5 fonemas menos grabados
                "bottom_fonemas": [
                    {"$match": {"metadata.fonema": {"$exists": True}}},
                    {"$group": {"_id": "$metadata.fonema", "total": {"$sum": 1}}},
                    {"$sort": {"total": 1}},
                    {"$limit": 5},
                    {"$project": {"_id": 0, "fonema": "$_id", "total": 1}}
                ],
            }
        }
    ]
    result = list(audio.aggregate(pipeline))[0]

    # Como ya tenemos los totales de cada etiqueta, mediante Python me quedo con los 5 de arriba y los 5 de abajo
    totales = result["totales_por_etiqueta"]  # ya ordenado de mayor a menor
    # Recorremos ultimas_etiquetas y le añadimos el total
    totales_map = {item["tag"]: item["total"] for item in totales}
    for tag in result["ultimas_etiquetas"]:
        tag["total"] = totales_map.get(tag["tag"], 0)

    syllabus = Syllabus()
    pipeline = [
        { '$unwind': { 'path': '$tags' } },
        { '$group': { '_id': '$tags', 'fecha': { '$last': '$fecha_creacion' }}},
        { '$sample': { 'size': 1 }}
    ]
    tags_suerte = syllabus.aggregate(pipeline)

    return render_template(
        'audios/client_tag.html',

        tags_suerte=tags_suerte,

        total_audios=result.get("total_audios", [{}]),
        ultimas_etiquetas=result.get("ultimas_etiquetas", []),
        top_etiquetas=totales[:5], 
        bottom_etiquetas=totales[-5:][::-1], 
        total_fonemas=result.get("total_fonemas", [{}]),
        ultimos_fonemas=result.get("ultimos_fonemas", []),
        top_fonemas=result.get("top_fonemas", []),
        bottom_fonemas=result.get("bottom_fonemas", []),
    )

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

    metadataOb = {}
    if text_id:
        # es un texto que proviene de una etiqueta
        regex = re.compile(r'^(\d{1,3})([a-zA-Z]+)([1-3])$')
        match = regex.match(text_tag)
        if match:
            num1, fonema, pos = match.groups()

            metadataOb = { # guardamos metadatos del tag para facilitar el entrenamiento
                "tipo_frase": "corta" if int(num1) >= 100 else "larga",
                "fonema": fonema.upper(),
                "posicion_lengua": {
                    "1": "baja",
                    "2": "media",
                    "3": "alta"
                }[pos]
            }
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
        "metadata": metadataOb,
        "schema_version": 2, # anyadimos los metadata en la v2
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
    ultimas_tags_grabadas = []
    mas_grabadas = []
    menos_grabadas = []
    ultimos_fonemas = []
    fonemas_mas_grabados = []
    fonemas_menos_grabados = []
    total_fonemas_unicos = 0
    logged_rol = current_user.rol
    url = 'audios/client_report.html'
    cliente_nombre = "N/A"

    PATRON_REGEX = r"^(\d+)([a-zA-ZñÑ]+)([1-3])$"

    audios_model = Audios()
    usuario_model = Usuario()

    if id or logged_rol == "cliente":
        # Cliente: un solo usuario (el propio o el indicado por parámetro)
        user_id = ObjectId(id) if id else current_user.id
        match_filter = {"usuario.id": user_id}

        cliente = usuario_model.find_one({"_id": user_id})
        cliente_nombre = cliente.get("nombre", "Desconocido") if cliente else "Desconocido"
    elif logged_rol == "tecnico":
        # Técnico: todos los clientes cuyo parent es el técnico de la sesión
        tecnico_email = current_user.email          
        clientes = usuario_model.find({"parent": tecnico_email})
        cliente_ids = [c["_id"] for c in clientes]

        match_filter = {"usuario.id": {"$in": cliente_ids}}
        cliente_nombre = "los usuarios supervisados"
    elif logged_rol == "admin":
        # Admin: no filtro por usuario → ve todos los audios
        match_filter = {}
        cliente_nombre = "Todos los usuarios"

    # ─────────────────────────────────────────────────────────────
    # 2. Pipeline único con $facet (independiente del rol)
    # ─────────────────────────────────────────────────────────────
    # Extracción del fonema reutilizada en varios puntos del pipeline
    _extract_fonema = {
        "$arrayElemAt": [
            {
                "$getField": {
                    "field": "captures",
                    "input": {
                        "$regexFind": {
                            "input": "$texto.tag",
                            "regex": PATRON_REGEX
                        }
                    }
                }
            },
            1   # capture group 1 → la parte alfabética del tag
        ]
    }

    pipeline = [
        {
            "$match": {
                **match_filter, # desempaquetamos el diccionario
                "texto.tag": {"$regex": PATRON_REGEX}
            }
        },
        {
            "$facet": {
                # ── Estadísticas básicas ──────────────────────────
                "tags": [
                    {"$group": {"_id": "$texto.tag", "cantidad": {"$sum": 1}}}
                ],
                "total_temp": [
                    {"$count": "valor"}
                ],

                # ── Últimas grabadas ──────────────────────────────
                "ultimas_grabadas": [
                    {"$sort": {"fecha": -1}},
                    {"$limit": 5},
                    {"$project": {"_id": 0, "tag": "$texto.tag"}}
                ],
                "ultimos_fonemas": [
                    {"$sort": {"fecha": -1}},
                    {"$limit": 5},
                    {"$project": {"_id": 0, "fonema": _extract_fonema}}
                ],

                # ── Top 5 tags ────────────────────────────────────
                "mas_grabadas": [
                    {"$group": {"_id": "$texto.tag", "cantidad": {"$sum": 1}}},
                    {"$sort": {"cantidad": -1}},
                    {"$limit": 5}
                ],
                "menos_grabadas": [
                    {"$group": {"_id": "$texto.tag", "cantidad": {"$sum": 1}}},
                    {"$sort": {"cantidad": 1}},
                    {"$limit": 5}
                ],

                # ── Top 5 fonemas ─────────────────────────────────
                "fonemas_mas_grabados": [
                    {"$group": {"_id": _extract_fonema, "cantidad": {"$sum": 1}}},
                    {"$sort": {"cantidad": -1}},
                    {"$limit": 5}
                ],
                "fonemas_menos_grabados": [
                    {"$group": {"_id": _extract_fonema, "cantidad": {"$sum": 1}}},
                    {"$sort": {"cantidad": 1}},
                    {"$limit": 5}
                ],

                # ── Fonemas únicos ────────────────────────────────
                "conteo_fonemas_unicos": [
                    {"$group": {"_id": _extract_fonema}},
                    {"$count": "total"}
                ]
            }
        },
        {
            "$project": {
                "tags": 1,
                "ultimas_grabadas": 1,
                "mas_grabadas": 1,
                "menos_grabadas": 1,
                "ultimos_fonemas": 1,
                "fonemas_mas_grabados": 1,
                "fonemas_menos_grabados": 1,
                "total": {
                    "$ifNull": [{"$arrayElemAt": ["$total_temp.valor", 0]}, 0]
                },
                "total_fonemas_unicos": {
                    "$ifNull": [{"$arrayElemAt": ["$conteo_fonemas_unicos.total", 0]}, 0]
                }
            }
        }
    ]

    resultado = list(audios_model.aggregate(pipeline))
    datos = resultado[0] if resultado else {}

    total_audios            = datos.get("total", 0)
    audios_por_categoria    = datos.get("tags", [])
    ultimas_tags_grabadas   = datos.get("ultimas_grabadas", [])
    mas_grabadas            = datos.get("mas_grabadas", [])
    menos_grabadas          = datos.get("menos_grabadas", [])
    ultimos_fonemas         = datos.get("ultimos_fonemas", [])
    fonemas_mas_grabados    = datos.get("fonemas_mas_grabados", [])
    fonemas_menos_grabados  = datos.get("fonemas_menos_grabados", [])
    total_fonemas_unicos    = datos.get("total_fonemas_unicos", 0)

    # Ordenar categorías por cantidad descendente (para el template)
    temp_dict = {item["_id"]: item["cantidad"] for item in audios_por_categoria}
    audios_por_categoria = dict(sorted(temp_dict.items(), key=lambda x: x[1], reverse=True))

    return render_template(
        url,
        total_audios=total_audios,
        audios_por_categoria=audios_por_categoria,
        usuario_id=id,
        cliente_nombre=cliente_nombre,
        rol=logged_rol,
        ultimas_tags_grabadas=ultimas_tags_grabadas,
        mas_grabadas=mas_grabadas,
        menos_grabadas=menos_grabadas,
        ultimos_fonemas=ultimos_fonemas,
        fonemas_mas_grabados=fonemas_mas_grabados,
        fonemas_menos_grabados=fonemas_menos_grabados,
        total_fonemas_unicos=total_fonemas_unicos
    )
