import certifi as certifi
from bson.objectid import ObjectId
from flask import current_app, g
from pymongo import ASCENDING
from pymongo import MongoClient
from werkzeug.local import LocalProxy

from pialara.models.User import User


# from project.models import User


def get_db():
    """
    Método de configuración para obtener una instancia de db
    """
    db = getattr(g, "_database", None)

    PIALARA_DB_URI = current_app.config["PIALARA_DB_URI"]
    PIALARA_DB_DB_NAME = current_app.config["PIALARA_DB_NAME"]

    if db is None:
        db = g._database = MongoClient(
            PIALARA_DB_URI,
            maxPoolSize=50,
            timeoutMS=2500,
            tlsCAFile = certifi.where()
        )[PIALARA_DB_DB_NAME]
    return db


# Utilizamos LocalProxy para leer la variable global usando sólo db
db = LocalProxy(get_db)


def get_all_users():
    """
    Devuelve una lista con todos los usuarios del sistema
    """
    try:
        return list(db.users.find({}).sort("nombre", ASCENDING))
    except Exception as e:
        return e


def get_user_by_id(id):
    """
    Devuelve un objeto User a partir de su id
    """
    try:
        usuario = db.usuarios.find_one({"_id": ObjectId(id)})

        usuario_obj = User(id=usuario["_id"],
                           mail=usuario.get("mail"),
                           nombre=usuario.get("nombre"),
                           password=usuario.get("password"),
                           rol=usuario.get("rol"),
                           parent=usuario.get("parent"))
        return usuario_obj
    except Exception as e:
        return e


def get_users(rol):
    """
    Devuelve una lista con los usuarios de un determinado rol
    """
    try:
        return list(db.users.find({"rol": rol}))
    except Exception as e:
        return e


def get_child_users_by_email(email):
    """
    Devuelve una lista con los usuarios cuyo padre contenga determinado email
    """
    try:
        return list(db.users.find({"parent": email}))
    except Exception as e:
        return e


def get_user(email):
    """
    Devuelve un objeto User
    Método a emplear en el login
    """
    try:
        usuario = db.usuarios.find_one({"mail": email})

        usuario_obj = User(id=usuario["_id"],
                           mail=usuario.get("mail"),
                           nombre=usuario.get("nombre"),
                           password=usuario.get("password"),
                           rol=usuario.get("rol"),
                           parent=usuario.get("parent"))
        print("Usuario objeto por email:", usuario_obj)

        return usuario_obj
    except Exception as e:
        print("Se ha producido un error", e)
        return None


def insert_user(user):
    """
    Inserta un usuario en la base de datos
    """
    try:
        doc = {"email": user.email,
               "password": user.password,
               "nombre": user.nombre,
               "rol": user.rol,
               "parent": user.parent}
        return db.users.insert_one(doc)
    except Exception as e:
        return e


def update_user(user):
    """
    Modifica un usuario (sólo atributos básicos)
    """
    try:
        expr = {"$set": {"nombre": user.nombre, "email": user.email, "rol": user.rol}}
        return db.users.update_one({"_id": ObjectId(user.id)}, expr)
    except Exception as e:
        return e


def delete_user(id):
    """
    Elimina un usuario por su id
    """
    try:
        return db.users.delete_one({"_id": ObjectId(id)})
    except Exception as e:
        return e