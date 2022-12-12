from urllib import request
from bson.objectid import ObjectId
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from pialara.decorators import rol_required
from pialara.models.Usuario import Usuario

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/')
@login_required
@rol_required(['admin', 'tecnico'])
def index():
    u = Usuario()

    users = []
    logged_rol = current_user.rol
    if logged_rol == "admin":
        users = u.find()
    else:
        users = u.find({"rol": {"$eq": 'cliente'}})

    return render_template('users/index.html', users=users, user_name='')


@bp.route('/', methods=['POST'])
@login_required
@rol_required(['admin', 'tecnico'])
def search_user():
    user_name = request.form.get('userName')
    u = Usuario()

    logged_rol = current_user.rol
    if logged_rol == "admin":
        users = u.find({'nombre': {"$regex": user_name, '$options': 'i'}})
    else:
        users = u.find({"rol": {"$eq": 'cliente'}, 'nombre': {"$regex": user_name, '$options': 'i'}})

    return render_template('users/index.html', users=users, user_name=user_name)

@bp.route('/create')
@login_required
def create():
    return render_template('users/create.html')


@bp.route('/update/<id>', methods=['GET'])
@login_required
def update(id):
    u = Usuario()
    model = u.find_one({'_id': ObjectId(id)})

    return render_template('users/update.html', model=model)


@bp.route('/update/<id>', methods=['POST'])
@login_required
def update_post(id):
    usu = Usuario()
    nombre = request.form.get('nombre')
    email = request.form.get('email')

    resultado = usu.update_one({'_id': ObjectId(id)}, {"$set": {'nombre': nombre, 'mail': email}})
    return render_template('users/index.html')


"""
@bp.route('/update', methods=['POST'])
@login_required
def updateData():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    password = request.form.get('password')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    sexo = request.form.get('sexo')
    provincia = request.form.get('provincia')
    enfermedades = request.form.get('enfermedades')
    dis = request.form.get('dis')

    result = db.update_user_all()
    print("Usuario modificado: ",result)
"""
"""@bp.route('/update/<id>', methods=['GET'])
@login_required
def update(id):
    u = Usuario()
    model=u.find_one({'_id': ObjectId(id)})
    if model is None:
        flash("usuario no existe", "error")
        return render_template('users/index.html')

    return render_template('users/update.html',model=model)"""
