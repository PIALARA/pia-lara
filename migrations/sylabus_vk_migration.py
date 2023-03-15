from pymongo import MongoClient
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

sylabus = []

with open('migrations/sylabus.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for fila in csv_reader:
        linea = {"texto": fila[1], "tags": ["syllabus",fila[0]],
            "creador": {"id": {"$oid": "639b4085a39c11c0c5121368"}, "nombre": "Aitor", "rol": "admin"},
            "fecha_creacion": datetime.today()}

        sylabus.append(linea)

try:
    db.sylabus.insert_many(sylabus)
except Exception as e:
    print(e)