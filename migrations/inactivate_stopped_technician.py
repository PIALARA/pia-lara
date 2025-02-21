import os
from datetime import datetime, timedelta

import bson
import configparser
import certifi as certifi
from pymongo import MongoClient
from werkzeug.security import generate_password_hash



config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("../.ini")))

if config['DEFAULT']['ENVIRONMENT'] == "Local":
    DB_URI = config['LOCAL']['PIALARA_DB_URI']
    DB_NAME = config['LOCAL']['PIALARA_DB_NAME']
else:
    DB_URI = config['PROD']['PIALARA_DB_URI']
    DB_NAME = config['PROD']['PIALARA_DB_NAME']


db = MongoClient(
    DB_URI,
    maxPoolSize = 50,
    timeoutMS = 2500,
    ssl=False
)[DB_NAME]

#################### MARCAR ACTIVO FALSE TECNICOS PARADOS ####################

# Extraemos los emails de los tecnicos asignados a usuarios

on_duty_technicians = db['usuarios'].distinct("parent", {"rol": "cliente"})

# Marcamos todos los tecnicos parados como activo: False

stopped_technicians = db['usuarios'].aggregate([{"$match":{ 'mail' : {"$nin": on_duty_technicians},  "rol": "tecnico"}}])


stopped_technicians_list = []

for stopped_technician in stopped_technicians:
    stopped_technicians_list.append(stopped_technician)

# Extraemos de la lista los _id de los tecnicos parados

ids_stopped_technicians = [x["_id"] for x in stopped_technicians_list]
print(ids_stopped_technicians)

set_active_false = db['usuarios'].update_many(
  {
    'rol': 'tecnico', 
    '_id': { "$in": ids_stopped_technicians} 
  },
  { "$set": {'activo': False}}
)

print(f"Usuarios actualizados: {set_active_false.modified_count}")

#################### MARCAR ACTIVO FALSE USUARIOS/TECNICOS ULTIMA CONEXION >12MESES ####################

hace_un_ano = datetime.now() - timedelta(days=365) 

resultado = db['usuarios'].update_many( {"ultima_conexion": {"$lt": hace_un_ano}}, {"$set": {"active": False}} )

print(f"Usuarios actualizados: {resultado.modified_count}")