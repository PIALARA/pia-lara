from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('syllabus', __name__, url_prefix='/syllabus')

from pialara.db import get_db
@bp.route('/')
def index():
    return render_template('syllabus/index.html')