#!/usr/bin/env python
# coding: utf-8

# TODO: Ejecutar Migracion para produccion.
# In[33]:


from pymongo import MongoClient
import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("../.ini")))

if config['DEFAULT']['ENVIRONMENT'] == "Local":
    DB_URI = config['LOCAL']['PIALARA_DB_URI']
    DB_NAME = config['LOCAL']['PIALARA_DB_NAME']
else:
    DB_URI = config['PROD']['PIALARA_DB_URI']
    DB_NAME = config['PROD']['PIALARA_DB_NAME']


client = MongoClient(
    DB_URI,
    maxPoolSize = 50,
    timeoutMS = 2500,
    ssl=False
)[DB_NAME]

tecnicos_asistentes = client['usuarios'].distinct("parent", {"rol": "cliente"})

print(tecnicos_asistentes)
print(f"Cantidad de técnicos actualmente asignados a clientes: {len(tecnicos_asistentes)}")


# In[28]:


# Vamos a consultar la cantidad de tecnicos que hay en la base de datos
lista_todos_tecnicos = []

todos_tecnicos = client['usuarios'].find({"rol":"tecnico"})

for tecnico in todos_tecnicos:
    lista_todos_tecnicos.append(tecnico)


print(f"Cantidad de tecnicos totales en la base de datos: {len(lista_todos_tecnicos)}")


# In[56]:


tecnicos_parados = client['usuarios'].aggregate([{"$match":{ 'mail' : {"$nin": tecnicos_asistentes},  "rol": "tecnico"}}])

tecnicos_parados_list = []

for tecnico_parado in tecnicos_parados:
    tecnicos_parados_list.append(tecnico_parado)


print(len(tecnicos_parados_list))
ids_tecnicos_parados = [x["_id"] for x in tecnicos_parados_list]

# Consultamos por asegurarnos si los ids extraidos pertenecen a tecnicos_asistentes

check_rol = client['usuarios'].find({"_id" : {"$in": ids_tecnicos_parados}}, {"rol": 1})

for rol in check_rol:
    if 'tecnico' not in rol["rol"]:
        print(f'El usuario con id {rol["_id"]} no es tecnico')
        


# ### Activo True / False

# In[ ]:


#Activos e inactivos

# ultima conexion 12 meses marcamos como inactivo
# Meter en el form en back o invisible la peticion de Activo true

# Activo = True / False

client['usuarios'].update_many(
  {'rol': 'cliente'}, 
  { "$set": {'activo': True}}
)


# In[61]:


tecnicos_parados = client['usuarios'].aggregate([{"$match":{ 'mail' : {"$nin": tecnicos_asistentes},  "rol": "tecnico"}}])

tecnicos_parados_list = []

for tecnico_parado in tecnicos_parados:
    tecnicos_parados_list.append(tecnico_parado)

ids_tecnicos_parados = [x["_id"] for x in tecnicos_parados_list]
print(ids_tecnicos_parados)

client['usuarios'].update_many(
  {
    'rol': 'tecnico', 
    '_id': { "$in": ids_tecnicos_parados} 
  },
  { "$set": {'activo': False}}
)


# In[63]:


client['usuarios'].update_many(
  {
    'rol': 'tecnico', 
    'mail': { "$in": tecnicos_asistentes} 
  },
  { "$set": {'activo': True}}
)

