from flask import Blueprint, render_template
from flask import (
    Blueprint, render_template, request
)


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
    return render_template('audios/create.html')

