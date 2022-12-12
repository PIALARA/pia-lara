from flask import Blueprint, render_template

bp = Blueprint('audios', __name__, url_prefix='/audios')

@bp.route('/create')
def index():
    return render_template('audios/create.html')

@bp.route('/create', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = db.get_user(email)
    # comprobamos si el usuario existe
    # cogemos la contraseña, la hasheamos y la comparamos con la contraseña hasheada
    if not user or not check_password_hash(user.password, password):
        flash('Por favor, comprueba tus datos y vuélvelo a intentar.')
        # si el usuario no existe, o está mal la contraseña, recargamos la página
        return redirect(url_for('auth.login'))

    # marcamos al usuario como autenticado en flask_login
    login_user(user, remember=remember)
    return redirect(url_for('auth.profile', nombre=current_user.nombre))
