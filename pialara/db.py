#importar mongodb

from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = 'conexion a mongo db'
        # venimos de aquí: https://flask.palletsprojects.com/en/2.2.x/tutorial/database/
        # sqlite3.connect(
        #     current_app.config['DATABASE'],
        #     detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()