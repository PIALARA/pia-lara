import certifi as certifi
from bson.objectid import ObjectId
from flask import current_app, g
from pymongo import ASCENDING
from pymongo import MongoClient
from werkzeug.local import LocalProxy

from datetime import datetime

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
            ssl=False
        )[PIALARA_DB_DB_NAME]
    return db


# Utilizamos LocalProxy para leer la variable global usando sólo db
db = LocalProxy(get_db)

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
                           ultima_conexion=usuario.get("ultima_conexion"),
                           parent=usuario.get("parent"),
						   activo=usuario.get("activo"))
													   
		  
				
		 
	   
        return usuario_obj
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
                           ultima_conexion=usuario.get("ultima_conexion"),
                           parent=usuario.get("parent"),
                           font_size=usuario.get("font_size"),
						   activo=usuario.get("activo"))
													   
						 
				
	   

        print("Usuario objeto por email:", usuario_obj)

        return usuario_obj
    except Exception as e:
        print("Se ha producido un error", e)
        return None


def update_ultima_conexion(email):
    """
    Devuelve un objeto User
    Método a emplear en el login
    """
    try:
        db.usuarios.update_one({"mail": email}, {"$set": {'ultima_conexion': datetime.now()}})
    except Exception as e:
        print("Se ha producido un error", e)
        return None
