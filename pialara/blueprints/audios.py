from flask import Blueprint, render_template
from flask import (
    Blueprint, render_template, request
)


bp = Blueprint('audios', __name__, url_prefix='/audios')

@bp.route('/create')
def index():
    return render_template('audios/create.html')

@bp.route('/save-record', methods=['POST'])
def save_record():
    file = request.files['file']
    return render_template('audios/create.html')

