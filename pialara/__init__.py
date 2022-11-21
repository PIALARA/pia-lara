from flask import Flask
import os
import configparser




def create_app():
    # create and configure the app
    app = Flask(__name__)

    config = configparser.ConfigParser()
    config.read(os.path.abspath(os.path.join("../.ini")))

    app.config['PIALARA_DB_URI'] = config['LOCAL']['PIALARA_DB_URI']
    app.config['PIALARA_DB_NAME'] = config['LOCAL']['PIALARA_DB_NAME']
    app.config['SECRET_KEY'] = config['LOCAL']['SECRET_KEY']

    config = configparser.ConfigParser()
    config.read(os.path.abspath(os.path.join("../.ini")))

    # Blueprints
    from pialara.blueprints import auth, syllabus
    app.register_blueprint(auth.bp)
    app.register_blueprint(syllabus.bp)

    # @app.route('/')
    # def index():
    #     return 'this is the index page'

    # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'

    return app
