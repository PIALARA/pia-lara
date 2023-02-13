import bson
import certifi as certifi
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

disfonias = [
    {
        "nombre": 'Disfonia 1',
        "visible" : 1
    },
    {
        "nombre": 'Disfonia 2',
        "visible" : 1
    },
    {
        "nombre": 'Disfonia 2',
        "visible" : 0
    }
]

disfoniasValidator = {
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
    db.drop_collection("disfonias")
    db.create_collection("disfonias", validator=disfoniasValidator)
    db.disfonias.insert_many(disfonias)
except Exception as e:
    print(e)