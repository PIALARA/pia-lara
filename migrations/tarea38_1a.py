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

# Patrón regex para tags
pattern = re.compile(r'^(\d{1,3})([A-Za-z]{1,2})(\d)$')

# Migración: syllabus
for doc in db.sylabus.find():
    tags = doc.get("tags", [])
    matching_tag = next((t for t in tags if pattern.match(t)), None)

    if matching_tag:
        match = pattern.match(matching_tag)
        numero_val = int(match.group(1))
        metadata = {
            "numero": "frase larga" if numero_val < 100 else "frase corta",
            "fonema": match.group(2),
            "posicion_lengua": {"1": "baja", "2": "media", "3": "alta"}.get(match.group(3))
        }
        db.sylabus.update_one({"_id": doc["_id"]}, {"$set": {"metadata": metadata}})

print("Migración completada en sylabus")

# Migración: audios
for doc in db.audios.find():
    texto_tag = doc.get("texto", {}).get("tag", "")
    match = pattern.match(texto_tag)

    if match:
        numero_val = int(match.group(1))
        metadata = {
            "tags": doc.get("tags", []),  # movemos tags existentes dentro de metadata
            "numero": "frase larga" if numero_val < 100 else "frase corta",
            "fonema": match.group(2),
            "posicion_lengua": {"1": "baja", "2": "media", "3": "alta"}.get(match.group(3))
        }
        db.audios.update_one(
            {"_id": doc["_id"]},
            {"$set": {"metadata": metadata}, "$unset": {"tags": ""}}  # eliminamos tags originales
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

export_collection_to_json("sylabus", "/home/mayury/Documentos/pia-lara/migrations/metadata_sylabus_export.json")
export_collection_to_json("audios", "/home/mayury/Documentos/pia-lara/migrations/metadata_audios_export.json")
