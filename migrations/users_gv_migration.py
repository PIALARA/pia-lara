from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import os
import configparser
from datetime import datetime
import csv

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

users = []

with open('migrations/users_gv2324b.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for fila in csv_reader:

        linea = {
            "fecha_nacimiento": datetime(2000, 1, 1),
            "mail": fila[0],
            "password": generate_password_hash("gv.com", method='sha256'),
            "rol": "tecnico",
            "nombre": fila[1],
            "sexo": fila[2],
            "ultima_conexion": datetime(2000, 1, 1)
        }

        users.append(linea)

try:
    db.usuarios.insert_many(users)
except Exception as e:
    print(e)