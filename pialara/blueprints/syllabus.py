from datetime import datetime
import math
import random
from bson.objectid import ObjectId
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from pialara.models.Syllabus import Syllabus
from pialara.models.Usuario import Usuario
from pialara.models.Clicks import Clicks

bp = Blueprint("syllabus", __name__, url_prefix="/syllabus")


def _get_momento_dia():
    hora = datetime.now().hour
    if 6 <= hora < 12:
        return "mañana"
    elif 12 <= hora < 20:
        return "tarde"
    return "noche"


def _get_frase_sugerida(syllabus, ubicacion):
    """
    Obtiene una frase sugerida optimizada usando $sample.
    """
    if ubicacion and ubicacion != "general":
        match = {"tags": {"$regex": ubicacion, "$options": "i"}}
    else:
        dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        dia_actual = dias_semana[datetime.now().weekday()]
        match = {"tags": {"$regex": dia_actual, "$options": "i"}}

    pipeline = [
        {"$match": match},
        {"$sample": {"size": 1}}
    ]
    
    try:
        resultado = list(syllabus.aggregate(pipeline))
        if resultado:
            return resultado[0]
    except Exception:
        pass

    # Fallback si no hay coincidencias o error: cualquier frase aleatoria
    try:
        fallback_pipeline = [{"$sample": {"size": 1}}]
        resultado_fallback = list(syllabus.aggregate(fallback_pipeline))
        return resultado_fallback[0] if resultado_fallback else None
    except Exception:
        return None

@bp.route("/", methods=["GET"])
@login_required
def index():
    tag_name = request.args.get("tagName") or ""
    tag_date_since = request.args.get("tagDateSince") or ""
    tag_date_to = request.args.get("tagDateTo") or ""
    current_page = int(request.args.get("page") or 1)

    syllabus = Syllabus()
    match_filter = {}

    if tag_name != "":
        match_filter.update(
            {
                "$or": [
                    {"tags": tag_name},
                    {"texto": {"$regex": tag_name, "$options": "i"}},
                ]
            }
        )
        
    # Agregamos un campo nuevo $expr para poder hacer un $and con los filtros de fecha
    match_filter.update({"$expr": {"$and": []}})
    
    if tag_date_since != "":
        match_filter["$expr"]["$and"].append(
            {
                "$lte": [
                    tag_date_since,
                    {
                        "$dateToString": {
                            "date": "$fecha_creacion",
                            "format": "%Y-%m-%d",
                        }
                    },
                ]
            }
        )

    if tag_date_to != "":
        match_filter["$expr"]["$and"].append(
            {
                "$gte": [
                    tag_date_to,
                    {
                        "$dateToString": {
                            "date": "$fecha_creacion",
                            "format": "%Y-%m-%d",
                        }
                    },
                ]
            }
        )

    pipeline = [{"$match": match_filter}]

    # Empieza modificacion
    PER_PAGE = 9

    total_pipeline = pipeline + [{"$count": "total"}]
    try:
        total = syllabus.aggregate(total_pipeline).next()["total"]
    except StopIteration:
        total = 0

    total_pages = math.ceil(total / PER_PAGE)
    skip = (current_page - 1) * PER_PAGE

    pipeline += [{"$skip": skip}, {"$limit": PER_PAGE}]
    print(pipeline)
    documentos = syllabus.aggregate(pipeline)

    pages_min = max([1, current_page - 3])
    pages_max = min([total_pages, pages_min + 5])

    if not documentos.alive:
        flash(
            "No se han encontrado resultados",
            "danger",
        )

    # Guardamos el click
    clicks = Clicks()
    click_doc = {
        "class": "syllabus",
        "method": "tag",
        "tag": tag_name,
        "dateSince": tag_date_since,
        "dateTo": tag_date_to,
        "usuario": current_user.email,
        "timestamp": datetime.now(),
    }
    clicks.insert_one(click_doc)

    # Lógica para frase sugerida (solo para clientes)
    ubicacion = request.args.get("location") or "general"
    momento_dia = _get_momento_dia()
    frase_sugerida = _get_frase_sugerida(syllabus, ubicacion)

    return render_template(
        "syllabus/index.html",
        syllabus=documentos,
        tag_name=tag_name,
        page=current_page,
        pages_min=pages_min,
        pages_max=pages_max,
        total_pages=total_pages,
        tag_date_since=tag_date_since,
        tag_date_to=tag_date_to,
        frase_sugerida=frase_sugerida,
        ubicacion=ubicacion,
        momento_dia=momento_dia,
    )


@bp.route("/frase-aleatoria", methods=["GET"])
@login_required
def frase_aleatoria():
    from flask import jsonify
    ubicacion = request.args.get("location") or "general"
    syllabus = Syllabus()
    frase = _get_frase_sugerida(syllabus, ubicacion)
    if not frase:
        return jsonify({"error": "No hay frases disponibles"}), 404
    return jsonify({
        "texto": frase.get("texto", ""),
        "tags": frase.get("tags", []),
        "momento_dia": _get_momento_dia(),
    })


@bp.route("/create")
@login_required
def create():
    return render_template("syllabus/create.html")




@bp.route("/create", methods=["POST"])
@login_required
def create_post():
    # Obtener los datos del formulario
    text = request.form.get("ftext")
    tags = request.form.get("ftags")

    # Obtener los datos del usuario
    usuario = Usuario()
    params = {"mail": current_user.email}
    user = usuario.find_one(params)

    # Convertir el array de los tags
    tagsArray = tags.split(", ")

    # Crear el texto en la base de datos
    texto = Syllabus()
    aux = {
        "texto": text,
        "creador": {
            "id": user.get("_id"),
            "nombre": user.get("nombre"),
            "rol": user.get("rol"),
        },
        "tags": tagsArray,
        "fecha_creacion": datetime.now(),
    }
    result = texto.insert_one(aux)

    # Comprobar el resultado y mostrar mensaje
    if result.acknowledged:
        flash("Texto creado correctamente", "success")
        return redirect(url_for("syllabus.index"))
    else:
        flash("La frase no se ha creado. Error genérico", "danger")
        return redirect(url_for("syllabus.create"))

@bp.route("/create_iterable")
@login_required
def create_iterable():
    return render_template("syllabus/create_iterable.html")

@bp.route("/create_iterable", methods=["POST"])
@login_required
def create_iterable_post():
    # Obtener los datos del formulario
    tags = request.form.get('ftags')
    if not tags or tags.strip() == "":
        flash('El campo de etiquetas no puede estar vacío.', 'danger')
        return redirect(url_for('syllabus.create_iterable'))

    
    qtyPhrases = request.form.get("qtyPhrases")

    # Recogemos todas las frases del formulario
    lista_frases = []
    for i in range(int(qtyPhrases)):
        lista_frases.append(request.form.get(f"ftext{i + 1}"))

    if not any("" == frase for frase in lista_frases) and qtyPhrases != 'Seleccionar':

        # Obtener los datos del usuario
        usuario = Usuario()
        params = {"mail": current_user.email}
        user = usuario.find_one(params)

        # Convertir el array de los tags
        tagsArray = tags.split(", ")
        texto = Syllabus()
        
        # Iteramos la lista de frases al reves
        for index ,text in enumerate(reversed(lista_frases)):
            if index == 0:
                print(f'Reversed lista {index}', text)
                # Crear el texto en la base de datos
                aux = {
                    "texto": text,
                    "creador": {
                        "id": user.get("_id"),
                        "nombre": user.get("nombre"),
                        "rol": user.get("rol"),
                    },
                    "tags": tagsArray,
                    "fecha_creacion": datetime.now(),
                    "iterable": {
                        "num": abs(index - len(lista_frases)),
                        "total": len(lista_frases)
                    }
                }
                result = texto.insert_one(aux)
                id_insertado = result.inserted_id  
                print("Frase ", text, "ID ", id_insertado)
            else:
                aux = {
                    "texto": text,
                    "creador": {
                        "id": user.get("_id"),
                        "nombre": user.get("nombre"),
                        "rol": user.get("rol"),
                    },
                    "tags": tagsArray,
                    "fecha_creacion": datetime.now(),
                    "iterable": {
                        "siguiente": id_insertado,
                        "num": abs(index - len(lista_frases)),
                        "total": len(lista_frases)
                    }
                }
                result = texto.insert_one(aux)
                id_insertado = result.inserted_id           
                print("Frase ", text, "ID ", id_insertado)
    
        flash("Iterable creado correctamente", "success")
        return redirect(url_for("syllabus.index"))
    else:
        flash("Campos erroneos!", "danger")
        return render_template("syllabus/create_iterable.html")
    

@bp.route("/update/<string:id>")
@login_required
def update(id):
    frase = Syllabus()
    params = {"_id": ObjectId(id)}
    syllabus = frase.find_one(params)

    aux = ""
    tags = syllabus.get("tags")
    for x in tags:
        aux = aux + ", " + x

    aux = aux[2:]

    return render_template("syllabus/update.html", syllabus=syllabus, tags=aux)


@bp.route("/update/<string:id>", methods=["POST"])
@login_required
def update_post(id):
    # Obtener los datos del formulario
    text = request.form.get("ftext")
    tags = request.form.get("ftags")
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
        flash("Texto actualizado correctamente", "success")
        return redirect(url_for("syllabus.index"))
    elif result.acknowledged & result.modified_count == 0:
        flash("Error al actualizar texto, inténtelo de nuevo...", "danger")
        return redirect(url_for("syllabus.update", id=fraseID))
    else:
        flash("La frase no se ha actualizado. Error genérico", "danger")
        return redirect(url_for("syllabus.index"))


@bp.route("/delete/<string:id>")
@login_required
def delete(id):
    frase = Syllabus()
    params = {"_id": ObjectId(id)}
    result = frase.delete_one(params)
    if result.acknowledged:
        flash("Frase eliminada correctamente", "success")
        return redirect(url_for("syllabus.index"))
    else:
        flash("La frase no se ha eliminado. Error genérico", "danger")
        return redirect(url_for("syllabus.index"))