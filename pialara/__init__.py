from flask import Flask
from flask_login import LoginManager
from pialara import db
import os
import configparser

def create_app():
    # create and configure the app
    app = Flask(__name__)
    config = configparser.ConfigParser()
    config.read(os.path.abspath(os.path.join(".ini")))
    #config.read('/var/www/pia-lara/.ini')

    app.config['PIALARA_DB_URI'] = config['LOCAL']['PIALARA_DB_URI']
    app.config['PIALARA_DB_NAME'] = config['LOCAL']['PIALARA_DB_NAME']
    app.config['SECRET_KEY'] = config['LOCAL']['SECRET_KEY']

    #app.config['AWS_ACCESS_KEY_ID'] = config['LOCAL']['AWS_ACCESS_KEY_ID']
    #app.config['AWS_SECRET_ACCESS_KEY'] = config['LOCAL']['AWS_SECRET_ACCESS_KEY']
    #app.config['BUCKET_NAME'] = config['LOCAL']['BUCKET_NAME']

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Blueprints
    from pialara.blueprints import auth, syllabus, users, audios, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(syllabus.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(audios.bp)
    app.register_blueprint(main.bp)

    @login_manager.user_loader
    def load_user(user_id):
        return db.get_user_by_id(user_id)

    return app