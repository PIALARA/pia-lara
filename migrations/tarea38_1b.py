from pymongo import MongoClient
import os
import configparser
from datetime import datetime
import csv
import re
import json
from bson.objectid import ObjectId

# Conexión a la base de datos PreLara (remota Atlas)
client = MongoClient("mongodb://prelara:pr3l4r4m3c@27.0.172.67/prelara")
db = client.prelara

# Función de normalización
def normalizar_texto(texto: str) -> str:
    if not texto:
        return ""

    texto = texto.upper()
    texto = re.sub(r'[.,\/#!$%\^&\*;:{}=\-_`~()¿?¡"]', '', texto)
    texto = texto.strip()
    texto = re.sub(r'\s+', '', texto)

    return texto

# Migración: SYLLABUS
for doc in db.sylabus.find({}, {"texto": 1}):
    texto_original = doc.get("texto", "")
    texto_normalizado = normalizar_texto(texto_original)

    db.sylabus.update_one(
        {"_id": doc["_id"]},
        {"$set": {"texto_normalizado": texto_normalizado}}
    )

print("Migración completada en sylabus")

# Migración: AUDIOS
for doc in db.audios.find({}, {"texto.texto": 1}):
    texto_original = doc.get("texto", {}).get("texto", "")
    texto_normalizado = normalizar_texto(texto_original)

    db.audios.update_one(
        {"_id": doc["_id"]},
        {"$set": {"texto_normalizado": texto_normalizado}}
    )

print("Migración completada en audios")

# Convierte a y guarda en JSON
def convert_for_json(obj):
    """
    Convierte ObjectId y datetime a string para JSON.
    """
    if isinstance(obj, dict):
        return {k: convert_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_for_json(i) for i in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()  # convierte datetime a ISO string
    else:
        return obj

def export_collection_to_json(collection_name, output_file):
    collection = db[collection_name]
    data = list(collection.find())
    data = convert_for_json(data)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Colección '{collection_name}' exportada a {output_file}")

export_collection_to_json("sylabus", "/home/mayury/Documentos/pia-lara/migrations/textoFormalizado_sylabus_export.json")
export_collection_to_json("audios", "/home/mayury/Documentos/pia-lara/migrations/textoFormalizado_audios_export.json")
