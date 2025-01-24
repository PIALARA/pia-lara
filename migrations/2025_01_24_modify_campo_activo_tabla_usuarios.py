#!/usr/bin/env python
# coding: utf-8

# In[33]:


from pymongo import MongoClient

client = MongoClient('mongodb://prelara:pr3l4r4m3c@27.0.172.67/prelara')
tecnicos_asistentes = client['prelara']['usuarios'].distinct("parent", {"rol": "cliente"})

print(tecnicos_asistentes)
print(f"Cantidad de técnicos actualmente asignados a clientes: {len(tecnicos_asistentes)}")


# In[28]:


# Vamos a consultar la cantidad de tecnicos que hay en la base de datos
lista_todos_tecnicos = []

todos_tecnicos = client['prelara']['usuarios'].find({"rol":"tecnico"})

for tecnico in todos_tecnicos:
    lista_todos_tecnicos.append(tecnico)


print(f"Cantidad de tecnicos totales en la base de datos: {len(lista_todos_tecnicos)}")


# In[56]:


tecnicos_parados = client['prelara']['usuarios'].aggregate([{"$match":{ 'mail' : {"$nin": tecnicos_asistentes},  "rol": "tecnico"}}])

tecnicos_parados_list = []

for tecnico_parado in tecnicos_parados:
    tecnicos_parados_list.append(tecnico_parado)


print(len(tecnicos_parados_list))
ids_tecnicos_parados = [x["_id"] for x in tecnicos_parados_list]

# Consultamos por asegurarnos si los ids extraidos pertenecen a tecnicos_asistentes

check_rol = client['prelara']['usuarios'].find({"_id" : {"$in": ids_tecnicos_parados}}, {"rol": 1})

for rol in check_rol:
    if 'tecnico' not in rol["rol"]:
        print(f'El usuario con id {rol["_id"]} no es tecnico')
        


# ### Activo True / False

# In[ ]:


#Activos e inactivos

# ultima conexion 12 meses marcamos como inactivo
# Meter en el form en back o invisible la peticion de Activo true

# Activo = True / False

client['prelara']['usuarios'].update_many(
  {'rol': 'cliente'}, 
  { "$set": {'activo': True}}
)


# In[61]:


tecnicos_parados = client['prelara']['usuarios'].aggregate([{"$match":{ 'mail' : {"$nin": tecnicos_asistentes},  "rol": "tecnico"}}])

tecnicos_parados_list = []

for tecnico_parado in tecnicos_parados:
    tecnicos_parados_list.append(tecnico_parado)

ids_tecnicos_parados = [x["_id"] for x in tecnicos_parados_list]
print(ids_tecnicos_parados)

client['prelara']['usuarios'].update_many(
  {
    'rol': 'tecnico', 
    '_id': { "$in": ids_tecnicos_parados} 
  },
  { "$set": {'activo': False}}
)


# In[63]:


client['prelara']['usuarios'].update_many(
  {
    'rol': 'tecnico', 
    'mail': { "$in": tecnicos_asistentes} 
  },
  { "$set": {'activo': True}}
)

