import datetime
from bson.objectid import ObjectId
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import current_user, login_required
from pialara.models.Audios import Audios
from pialara.models.Usuario import Usuario


bp = Blueprint('logros', __name__, url_prefix='/logros')

@bp.route('/')
def index():
    correo_usuario_actual = str(current_user.email)
    print(correo_usuario_actual)
    usuarios_model = Usuario()
    queryuser = { "mail": correo_usuario_actual } 
    usuario = usuarios_model.find_one(queryuser)
    logros = usuario.get("logros", [])
    audios_model = Audios()  

    
    pipeline = [
        {
            '$group': {
                '_id': '$texto.tag',
                'cantidad': {
                    '$sum': 1
                }
            }
        },
        {
            '$sort': {
                'cantidad': -1
            }
        }
    ]
 
    result = audios_model.aggregate(pipeline)

    return render_template('logros/index.html', aggregation_result=result,logros=logros)