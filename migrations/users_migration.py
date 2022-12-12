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

db = MongoClient(DB_URI)[DB_NAME]

usuarios = [{
    "fecha_nacimiento": datetime(1998, 5, 17),
    "mail": "rococo@gmail.com",
    "password": generate_password_hash("admin", method='sha256'),
    "rol": "admin",
    "nombre": "Rocío",
    "sexo": "M",
    "ultima_conexion": datetime.today()
},
    {
        "fecha_nacimiento": datetime(1989, 5, 17),
        "mail": "mario@gmail.com",
        "password": generate_password_hash("admin", method='sha256'),
        "rol": "cliente",
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
        "mail": "ines@gmail.com",
        "password": generate_password_hash("admin", method='sha256'),
        "rol": "tecnico",
        "nombre": "Inés",
        "sexo": "M",
        "ultima_conexion": datetime.today()

    },
    {
        "fecha_nacimiento": datetime(1997, 2, 4),
        "mail": "pedro@gmail.com",
        "password": generate_password_hash("admin", method='sha256'),
        "rol": "cliente",
        "nombre": "Pedro",
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
        "fecha_nacimiento": datetime(1996, 3, 1),
        "mail": "pedro@gmail.com",
        "password": generate_password_hash("admin", method='sha256'),
        "rol": "cliente",
        "nombre": "Pedro",
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
        "fecha_nacimiento": datetime(1945, 2, 12),
        "mail": "pedro@gmail.com",
        "password": generate_password_hash("admin", method='sha256'),
        "rol": "cliente",
        "nombre": "Hector",
        "sexo": "H",
        "provincia": "Madrid",
        "ultima_conexion": datetime.today(),
        "enfermedades": [
            "iptus"
        ],
        "dis": [
            "dislexia"
        ]
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
                    'H'
                ]
            }
        }
    }
}

sylabus = [
    {
        "_id": bson.objectid.ObjectId("637a078e8659dd172e6afaf5"),
        "texto": "Esto es una prueba",
        "creador": {
            "id": bson.objectid.ObjectId("6379fc6871880707a2c89537"),
            "nombre": "Rocio",
            "rol": "admin"
        },
        "tags": [
            "dislalia",
            "paralisis facial",
            "futbol",
            "madrid"
        ],
        "audios": [
            {
                "id": bson.objectid.ObjectId("637a08118659dd172e6afafa")
            },
            {
                "id": bson.objectid.ObjectId("637a08208659dd172e6afafb")
            },
            {
                "id": bson.objectid.ObjectId("637a08388659dd172e6afafc")
            }
        ],
        "fecha_creacion": datetime.today()
    },

    {
        "_id": bson.objectid.ObjectId("638348e9b3ba0b56509dfa1b"),
        "texto": "Esto es una prueba 2",
        "creador": {
            "id": bson.objectid.ObjectId("637fd98b2950843403bd5d8a"),
            "nombre": "Mario",
            "rol": "cliente"
        },
        "tags": [
            "dislalia",
            "paralisis facial",
            "futbol",
            "madrid"
        ],
        "audios": [
            {
                "id": bson.objectid.ObjectId("6379ff018659dd172e6afadc"),

            }
        ],
        "fecha_creacion": datetime.today()
    }
]

sylabusValidator = {
    "$jsonSchema": {
        "required": [
            'texto',
            'creador',
            'fecha_creacion'
        ],
        "properties": {
            "texto": {
                "bsonType": 'string'
            },
            "creador": {
                "bsonType": 'object'
            },
            "tags": {
                "bsonType": 'array'
            },
            "fecha_creacion": {
                "bsonType": 'date'
            }
        }
    }
}

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
                "id":bson.objectid.ObjectId("637fb70f9297829bcac1be50"),
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
            "id":bson.objectid.ObjectId("637a02b38659dd172e6afae4"),
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
            'texto',
            'usuario',
            'aws_object_id'
        ],
        "properties": {
            "texto": {
                "bsonType": 'object'
            },
            "usuario": {
                "bsonType": 'object'
            },
            "duracion": {
                "bsonType": 'int'
            },
            "fecha": {
                "bsonType": 'date'
            },
            "notas": {
                "bsonType": 'string'
            },
            "valoracion": {
                "bsonType": 'int',
                'enum': [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5
                ]
            }
        }
    }
}

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
    db.drop_collection("usuarios")
    db.create_collection("usuarios", validator=userValidator)
    db.usuarios.insert_many(usuarios)

    db.drop_collection("sylabus")
    db.create_collection("sylabus", validator=sylabusValidator)
    db.sylabus.insert_many(sylabus)

    db.drop_collection("audios")
    db.create_collection("audios", validator=audioValidator)
    db.audios.insert_many(audio)

    db.drop_collection("enfermedades")
    db.create_collection("enfermedades", validator=enfermedadesValidator)
    db.enfermedades.insert_many(enfermedades)

    db.drop_collection("disfonias")
    db.create_collection("disfonias", validator=disfoniasValidator)
    db.disfonias.insert_many(disfonias)
except Exception as e:
    print(e)
