from flask import Blueprint, render_template

bp = Blueprint('audios', __name__, url_prefix='/audios')

@bp.route('/create')
def index():
    return render_template('audios/create.html')