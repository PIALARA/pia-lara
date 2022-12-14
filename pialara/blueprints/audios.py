import os.path

from flask import Blueprint, render_template
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from pialara.models.Syllabus import Syllabus


bp = Blueprint('audios', __name__, url_prefix='/audios')

@bp.route('/client-tag')
@login_required
def client_tag():
    syllabus = Syllabus()
    pipeline = [
        {
            '$unwind': {
                'path': '$tags'
            }
        }, {
            '$group': {
                '_id': '$tags',
                'total': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                'total': -1
            }
        }
    ]

    tags = syllabus.aggregate(pipeline)

    return render_template('audios/client_tag.html', tags=tags)

@bp.route('/client-record/<string:tag_name>')
@login_required
def client_record(tag_name):
    return render_template('audios/create.html', tag_name=tag_name)

@bp.route('/client-text')
@login_required
def client_text():
    return render_template('audios/client_text.html')

## @todo deleteme
@bp.route('/create')
@login_required
def index():
    return render_template('audios/create.html')

@bp.route('/save-record', methods=['POST'])
@login_required
def save_record():
    file = request.files['file']
    # Hemos pensado en guardar timestamp + id de usuario. Ver si se guarda en mp3 o wav
    print(current_user.id)
    filename = secure_filename('prueba.wav')
    file.save(os.path.join('./', filename))
    print(file)
    return render_template('audios/create.html')


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
            '$group': {
                '_id': '$tags',
                'total': {
                    '$sum': 1
                }
            }
        }, {
            '$match': {
                '_id': {'$regex': tag_name, '$options': 'i'}
            }
        }
    ]

    tags = syllabus.aggregate(pipeline)

    if not tags.alive:
        flash("No se han encontrado resultados de la etiqueta '" + tag_name + "'", "danger")

    return render_template('audios/client_tag.html', tags=tags, tag_name=tag_name)


@bp.route('/tag/<string:tag>')
@login_required
#Sin uso
def tag_syllabus(tag):
    syllabus = Syllabus()

    pipeline = [
        {
            '$unwind': {
                'path': '$tags'
            }
        }, {
            '$match': {
                'tags': {'$regex': tag, '$options': 'i'}
            }
        }
    ]

    frases = syllabus.aggregate(pipeline)

    if not frases.alive:
        flash("No se han encontrado frases con la etiqueta '" + tag + "'", "danger")

    return render_template('audios/create.html', frases=frases, tag=tag)

