from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

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