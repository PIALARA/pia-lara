import re
from pymongo import MongoClient



def normalizar(texto: str) -> str:
    texto = texto.upper().strip()
    #eliminar puntuación al inicio y al final
    texto = re.sub(r'^[^\w]+|[^\w]+$', '', texto)
    return texto

def add_texto_normalizado():
    syllabus_modificados = 0
    audios_modificados = 0

    #Colección Syllabus normalizando la primera etiqueta
    for doc in db.syllabus.find({"tags": {"$exists": True}}):
        if doc.get("tags"):
            texto_norm = normalizar(doc["tags"][0])
            result = db.syllabus.update_one(
                {"_id": doc["_id"], "texto_normalizado": {"$exists": False}},
                {"$set": {"texto_normalizado": texto_norm}}
            )
            syllabus_modificados += result.modified_count

    #Colección audio normalizando texto.tag
    for doc in db.audios.find({"texto.tag": {"$exists": True}}):
        texto_norm = normalizar(doc["texto"]["tag"])
        result = db.audios.update_one(
            {"_id": doc["_id"], "texto_normalizado": {"$exists": False}},
            {"$set": {"texto_normalizado": texto_norm}}
        )
        audios_modificados += result.modified_count

    print("Migración texto_normalizado completada")
    print(f"Syllabus modificados: {syllabus_modificados}")
    print(f"Audios modificados: {audios_modificados}")

if __name__ == "__main__":
    add_texto_normalizado()
