from _curses import flash
from urllib import request

from flask_login import login_required, current_user
from pialara.models.Usuario import Usuario
from bson.objectid import ObjectId
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/')
@login_required
def index():
    u = Usuario()

    # logged_rol = current_user.rol
    # if logged_rol == "Administrador":
    #     users = db.users.find()
    # else:
    #     raise Exception("Operación no permitida para el rol", logged_rol)

    return render_template('users/index.html', users=u.find())


@bp.route('/create')
@login_required
def create():
    return render_template('users/create.html')

@bp.route('/update/<id>', methods=['GET'])
@login_required
def update(id):
    u = Usuario()
    model=u.find_one({'_id': ObjectId(id)})
   
    return render_template('users/update.html',model=model)

@bp.route('/update/<id>', methods=['POST'])
@login_required
def update_post(id):
    usu = Usuario()
    nombre = request.form.get('nombre')
    email = request.form.get('email')

    resultado = usu.update_one({'_id': ObjectId(id)},{"$set":{'nombre':nombre, 'mail':email}})

    if resultado.acknowledged & resultado.modified_count == 1:
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('users.index'))
    elif resultado.acknowledged & resultado.modified_count == 0:
        flash('Error al actualizar el usuario, inténtelo de nuevo...', 'danger')
        return redirect(url_for('users.update', id=id))
    else:
        flash('La usuario no se ha actualizado. Error genérico', 'danger')
        return redirect(url_for('users.index'))


