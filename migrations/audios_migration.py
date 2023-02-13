import bson
from pymongo import MongoClient
import certifi as certifi
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
    maxPoolSize=50,
    timeoutMS=2500,
    ssl=False
)[DB_NAME]

audio = [
    {
        "_id": bson.objectid.ObjectId("6379ff018659dd172e6afadc"),
        "fecha": datetime.today(),
        "texto": {
            "id": bson.objectid.ObjectId("638348e9b3ba0b56509dfa1b"),
            "texto": "Esto es una prueba 2",
            "creador": {
                "id": bson.objectid.ObjectId("637fb70f9297829bcac1be50"),
                "rol": "cliente",
                "nombre": "Sebas"
            },
            "tags": [
                "dislalia",
                "paralisis facial",
                "futbol",
                "madrid"
            ]
        },
        "usuario": {
            "enfermedad": [
                "paralisis"
            ],
            "id": bson.objectid.ObjectId("637a02b38659dd172e6afae4"),
            "sexo": "H",
            "provincia": "alicante",
            "edad": 42,
            "nombre": "Jesús",
            "dis": [
                "dislalia"
            ]
        },
        "duracion": 60,
        "notas": "en esta sesion a lo mejor ha habido mucho ruido",
        "valoracion": 4,
        "aws_object_id": "https://audio.com/"
    },

    {
        "_id": bson.objectid.ObjectId("638351f7b3ba0b56509dfa6b"),
        "fecha": datetime.today(),
        "texto": {
            "id": bson.objectid.ObjectId("638348e9b3ba0b56509dfa1b"),
            "texto": "Esto es una prueba 2",
            "creador": {
                "id": bson.objectid.ObjectId("637fb70f9297829bcac1be50"),
                "rol": "cliente",
                "nombre": "Sebas"
            },
            "tags": [
                "dislalia",
                "paralisis facial",
                "futbol",
                "madrid"
            ]
        },
        "usuario": {
            "enfermedad": [
                "paralisis"
            ],
            "id": bson.objectid.ObjectId("637a02b38659dd172e6afae4"),
            "sexo": "H",
            "provincia": "alicante",
            "edad": 42,
            "nombre": "Jesús",
            "dis": [
                "dislalia"
            ]
        },
        "duracion": 60,
        "notas": "en esta sesion a lo mejor ha habido mucho ruido",
        "valoracion": 4,
        "aws_object_id": "https://audio.com/"
    }

]
audioValidator = {

    "$jsonSchema": {
        "required": [
            'fecha',
            'aws_object_id'
        ],
        "properties": {
            "duracion": {
                "bsonType": 'int'
            },
            "fecha": {
                "bsonType": 'date'
            }
        }
    }
}

try:
    db.drop_collection("audios")
    db.create_collection("audios", validator=audioValidator)
    db.audios.insert_many(audio)
    print('Correcto')
except Exception as e:
    print(e)
