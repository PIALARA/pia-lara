import certifi as certifi
import bson
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import os
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

# DB_URI = config['PROD']['PIALARA_DB_URI']
# DB_NAME = config['PROD']['PIALARA_DB_NAME']
DB_URI = config['LOCAL']['PIALARA_DB_URI']
DB_NAME = config['LOCAL']['PIALARA_DB_NAME']

db = MongoClient(
    DB_URI,
    maxPoolSize = 50,
    timeoutMS = 2500,
    ssl=False
)[DB_NAME]

enfermedades = [
    {
        "nombre": 'Enfermedad 1',
        "visible" : 1
    },
    {
        "nombre": 'Enfermedad 2',
        "visible" : 1
    },
    {
        "nombre": 'Enfermedad 2',
        "visible" : 0
    }
]

enfermedadesValidator = {
    "$jsonSchema": {
        "required": [
            'nombre',
            'visible'
        ],
        "properties": {
            "nombre": {
                "bsonType": 'string'
            },
            "visible": {
                "bsonType": 'int'
            }
        }
    }
}

try:
    db.drop_collection("enfermedades")
    db.create_collection("enfermedades", validator=enfermedadesValidator)
    db.enfermedades.insert_many(enfermedades)
except Exception as e:
    print(e)