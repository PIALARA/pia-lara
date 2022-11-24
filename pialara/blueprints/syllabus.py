from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('syllabus', __name__, url_prefix='/syllabus')

from pialara.db import get_db
@bp.route('/')
def index():
    return render_template('syllabus/index.html')

"""
@bp.route('/create/:id')
def create():
    return render_template('syllabus/create.html')

@bp.route('/create/:id', methods=['post'])
def create_post():
    flash('creado correctamente')
    redirect('/create')

@bp.route('/update/:id')
def update():
    return render_template('syllabus/update.html')

@bp.route('/update/:id', methods=['post'])
def update_post():
    flash('modificado correctamente')
    redirect('/update')


@bp.route('/delete/:id')
def delete():
    return render_template('syllabus/index.html')

@bp.route('/view/:id')
def view():
    return render_template('syllabus/index.html')
"""
