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

usuarios = [{
    "fecha_nacimiento": datetime(1998, 5, 17),
    "mail": "cliente@cliente.com",
    "password": generate_password_hash("cliente", method='sha256'),
    "rol": "cliente",
    "nombre": "Rocío",
    "sexo": "M",
    "parent": "tecnico@tecnico.com",
    "ultima_conexion": datetime.today()
},
{
    "fecha_nacimiento": datetime(1998, 5, 17),
    "mail": "clienteFake@clienteFake.com",
    "password": generate_password_hash("cliente", method='sha256'),
    "rol": "cliente",
    "nombre": "Cliente sin tecnico",
    "sexo": "M",
    "parent": "uncorreo@uncorreo.com",
    "ultima_conexion": datetime.today()
},
    {
        "fecha_nacimiento": datetime(1989, 5, 17),
        "mail": "admin@admin.com",
        "password": generate_password_hash("admin", method='sha256'),
        "rol": "admin",
        "nombre": "Mario",
        "sexo": "H",
        "provincia": "Alicante",
        "ultima_conexion": datetime.today(),
        "enfermedades": [
            "paralisis facial"
        ],
        "dis": [
            "disfemia"
        ]
    },
    {
        "fecha_nacimiento": datetime(1957, 4, 21),
        "mail": "tecnico@tecnico.com",
        "password": generate_password_hash("tecnico", method='sha256'),
        "rol": "tecnico",
        "nombre": "Inés",
        "sexo": "M",
        "ultima_conexion": datetime.today()

    },
    {
        "fecha_nacimiento": datetime(1957, 4, 21),
        "mail": "tecnico2@tecnico.com",
        "password": generate_password_hash("tecnico", method='sha256'),
        "rol": "tecnico",
        "nombre": "Alberto",
        "sexo": "M",
        "ultima_conexion": datetime.today()

    }
]

userValidator = {
    "$jsonSchema": {
        "required": [
            'password',
            'mail',
            'nombre',
            'rol',
            'fecha_nacimiento',
            'ultima_conexion'
        ],
        "properties": {
            "mail": {
                "bsonType": 'string'
            },
            "parent": {
                "bsonType": 'string'
            },
            "password": {
                "bsonType": 'string'
            },
            "id": {
                "bsonType": 'objectId'
            },
            "fecha_nacimiento": {
                "bsonType": 'date'
            },
            "ultima_conexion": {
                "bsonType": 'date'
            },
            "nombre": {
                "bsonType": 'string'
            },
            "rol": {
                "bsonType": 'string',
                'enum': [
                    "admin",
                    "tecnico",
                    "cliente"
                ]
            },
            "provincia": {
                "bsonType": 'string',
                'enum': [
                    'A Coruña',
                    'Álava',
                    'Albacete',
                    'Alicante',
                    'Almería',
                    'Asturias',
                    'Ávila',
                    'Badajoz',
                    'Baleares',
                    'Barcelona',
                    'Burgos',
                    'Cáceres',
                    'Cádiz',
                    'Cantabria',
                    'Castellón',
                    'Ciudad Real',
                    'Córdoba',
                    'Cuenca',
                    'Girona',
                    'Granada',
                    'Guadalajara',
                    'Gipuzkoa',
                    'Huelva',
                    'Huesca',
                    'Jaén',
                    'La Rioja',
                    'Las Palmas',
                    'León',
                    'Lérida',
                    'Lugo',
                    'Madrid',
                    'Málaga',
                    'Murcia',
                    'Navarra',
                    'Ourense',
                    'Palencia',
                    'Pontevedra',
                    'Salamanca',
                    'Segovia',
                    'Sevilla',
                    'Soria',
                    'Tarragona',
                    'Santa Cruz de Tenerife',
                    'Teruel',
                    'Toledo',
                    'Valencia',
                    'Valladolid',
                    'Vizcaya',
                    'Zamora',
                    'Zaragoza',
                    'Ceuta',
                    'Melilla'
                ]
            },
            "sexo": {
                "bsonType": 'string',
                'enum': [
                    'M',
                    'H',
                    'A',
                    'T'
                ]
            }
        }
    }
}

try:
    db.drop_collection("usuarios")
    db.create_collection("usuarios", validator=userValidator)
    db.usuarios.insert_many(usuarios)

except Exception as e:
    print(e)