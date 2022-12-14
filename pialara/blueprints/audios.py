import os.path

from flask import Blueprint, render_template
from flask import (
    Blueprint, render_template, request
)
from flask_login import current_user
from werkzeug.utils import secure_filename

bp = Blueprint('audios', __name__, url_prefix='/audios')

@bp.route('/client-tag')
def client_tag():
    return render_template('audios/client_tag.html')

@bp.route('/client-record')
def client_record():
    return render_template('audios/client_record.html')

@bp.route('/client-text')
def client_text():
    return render_template('audios/client_text.html')

## @todo deleteme
@bp.route('/create')
def index():
    return render_template('audios/create.html')

@bp.route('/save-record', methods=['POST'])
def save_record():
    file = request.files['file']
    # Hemos pensado en guardar timestamp + id de usuario. Ver si se guarda en mp3 o wav
    print(current_user.id)
    filename = secure_filename('prueba.wav')
    file.save(os.path.join('./', filename))
    print(file)
    return render_template('audios/create.html')

